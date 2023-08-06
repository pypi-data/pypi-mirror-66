import logging
import os
import sys
import threading
import time

from nerdvision import settings
from nerdvision.ContextUploadService import ContextUploadService
from nerdvision.FrameProcessor import FrameProcessor
from nerdvision.models.EventSnapshot import Watcher

our_logger = logging.getLogger("nerdvision")


class BreakpointService(object):

    def __init__(self, set_trace=True):
        self.breakpoints = {}
        self.var_id = 1
        self.context_service = ContextUploadService()
        self.session_id = None
        self.rate_limit_tracker = {}
        if set_trace:
            sys.settrace(self.trace_call)
            threading.settrace(self.trace_call)

    def trace_call(self, frame, event, arg):
        if len(self.breakpoints) == 0:
            return None

        lineno = frame.f_lineno
        filename = frame.f_code.co_filename

        breakpoints_for = self.breakpoints_for(filename)

        if settings.is_point_cut_debug_enabled():
            our_logger.debug("Found %s breakpoints for %s", len(breakpoints_for), filename)

        if event == "call" and len(breakpoints_for) == 0:
            return None

        if event == "line":
            bps_ff, bps_sf, bps_nf, bps_log = self.find_match(breakpoints_for, lineno, frame)

            if len(bps_ff) > 0 or len(bps_sf) > 0 or len(bps_nf) > 0:
                max_collection_size, max_string_length, max_variables, max_variable_depth = self.get_breakpoint_config(
                    bps_ff + bps_sf + bps_nf)

                processor = FrameProcessor(max_variable_depth, max_collection_size, max_string_length, max_variables)

                if len(bps_sf) > 0 and len(bps_ff) == 0:
                    processor.process_back_frame_vars = False

                if len(bps_ff) > 0 or len(bps_sf) > 0:
                    processor.process_frame(frame)

                for bp in bps_ff:
                    self.process_watches(bp, frame, processor)
                    bp_map = self.bp_as_map(bp)
                    self.add_rate_limit_info(bp, bp_map)
                    self.context_service.send_event(processor.event, bp_map, processor.watchers, self.session_id)

                if len(bps_ff) > 0:
                    for i, sf in enumerate(processor.event.stack_trace):
                        if i > 0:
                            sf.variables = []

                for bp in bps_sf:
                    self.process_watches(bp, frame, processor)
                    bp_map = self.bp_as_map(bp)
                    self.add_rate_limit_info(bp, bp_map)
                    self.context_service.send_event(processor.event, bp_map, processor.watchers, self.session_id)

                # Clear current frame before doing no_frame breakpoint so we send less data
                processor.event.stack_trace = []
                for bp in bps_nf:
                    self.process_watches(bp, frame, processor)
                    bp_map = self.bp_as_map(bp)
                    self.add_rate_limit_info(bp, bp_map)
                    self.context_service.send_event(processor.event, bp_map, processor.watchers, self.session_id)
                    processor.watchers = []

            if len(bps_log) > 0:
                for bp_log in bps_log:
                    self.process_log_point(bp_log, frame)

        return self.trace_call

    def add_rate_limit_info(self, bp, bp_map):
        rate_limit_info = self.rate_limit_tracker[bp.breakpoint_id]
        bp_map['args']['suppressed_count'] = rate_limit_info['suppressed_count']
        # reset suppressed count here rather than below since now we added it to the bp dict
        rate_limit_info['suppressed_count'] = 0

    def next_id(self):
        self.var_id = self.var_id + 1
        return self.var_id

    def process_request(self, response, session_id):
        self.session_id = session_id
        our_logger.debug("Processing breakpoints %s", response)
        new_breakpoints = {}
        for _breakpoint in response.breakpoints:
            if _breakpoint.args['class'] in new_breakpoints:
                new_breakpoints[_breakpoint.args['class']].append(_breakpoint)
            else:
                new_breakpoints[_breakpoint.args['class']] = [_breakpoint]
        self.breakpoints = new_breakpoints
        # Decision made for now just clean the rate limits for everything when new breakpoints come in
        self.rate_limit_tracker = {}
        our_logger.debug("New breakpoint configuration %s", self.breakpoints)

    def breakpoints_for(self, filename):
        basename = os.path.basename(filename)

        if settings.is_point_cut_debug_enabled():
            our_logger.debug("Searching for breakpoint for %s", basename)

        if basename in self.breakpoints:
            breakpoints_basename_ = self.breakpoints[basename]
            return breakpoints_basename_
        else:
            return []

    def find_match(self, breakpoints_for, lineno, frame):
        switcher = {
            'stack': [],
            'no_frame': [],
            'frame': [],
            'log_point': []
        }

        for bp in breakpoints_for:
            if bp.line_no == lineno and self.condition_matches(bp, frame) and self.can_fire(bp):
                if bp.type in switcher:
                    switcher.get(bp.type).append(bp)
                else:
                    switcher.get('frame').append(bp)

        return switcher['stack'], switcher['frame'], switcher['no_frame'], switcher['log_point']

    def get_breakpoint_config(self, breakpoints):
        max_collection_size = -1
        max_string_length = -1
        max_variables = -1
        max_variable_depth = -1

        for bp in breakpoints:
            tmp_max_col_size = bp.args['MAX_COLLECTION_SIZE']
            tmp_max_string_length = bp.args['MAX_STRING_LENGTH']
            tmp_max_variables = bp.args['MAX_VARIABLES']
            tmp_max_var_depth = bp.args['MAX_VAR_DEPTH']

            max_collection_size = self.get_max_value(max_collection_size, tmp_max_col_size)
            max_string_length = self.get_max_value(max_string_length, tmp_max_string_length)
            max_variables = self.get_max_value(max_variables, tmp_max_variables)
            max_variable_depth = self.get_max_value(max_variable_depth, tmp_max_var_depth)

            if max_collection_size == -1:
                max_collection_size = FrameProcessor.default_max_list_len
            if max_string_length == -1:
                max_string_length = FrameProcessor.default_max_str_length
            if max_variables == -1:
                max_variables = FrameProcessor.default_max_vars
            if max_variable_depth == -1:
                max_variable_depth = FrameProcessor.default_max_depth

        return max_collection_size, max_string_length, max_variables, max_variable_depth

    def can_fire(self, bp):
        if self.rate_limit_hit(bp):
            return False

        if bp.fire_count >= 0:
            if self.rate_limit_tracker[bp.breakpoint_id]['fire_count'] >= bp.fire_count:
                return False
            self.rate_limit_tracker[bp.breakpoint_id]['fire_count'] += 1
        return True

    def rate_limit_hit(self, bp):
        millis = int(round(time.time() * 1000))
        rate_limit = bp.args['rate_limit'] or settings.nv_settings['bp_rate_limit']

        if bp.breakpoint_id in self.rate_limit_tracker:
            bp_data = self.rate_limit_tracker[bp.breakpoint_id]

            if (millis - bp_data['last_fired']) < int(rate_limit):
                bp_data['suppressed_count'] += 1
                return True
            else:
                bp_data['last_fired'] = millis
                return False

        self.rate_limit_tracker[bp.breakpoint_id] = {'last_fired': millis,
                                                     'suppressed_count': 0,
                                                     'fire_count': 0}
        return False

    @staticmethod
    def get_max_value(item, compare):
        if compare.isdigit():
            compare = int(compare)
            if compare > item:
                return compare
            else:
                return item
        return -1

    @staticmethod
    def condition_matches(bp, frame):
        if bp.condition is None or bp.condition == "":
            # There is no condition so return True
            return True
        our_logger.debug("Executing condition evaluation: %s", bp.condition)
        try:
            result = eval(bp.condition, None, frame.f_locals)
            our_logger.debug("Condition result: %s", result)
            if result:
                return True
            return False
        except Exception:
            our_logger.exception("Error evaluating condition %s", bp.condition)
            return False

    @staticmethod
    def process_watches(bp, frame, processor):
        watches = bp.named_watchers
        for watch in watches:
            watch_ = watches[watch]
            our_logger.debug("Evaluating watcher: %s -> %s", watch, watch_)
            if watch_ != "":
                try:
                    eval_result = eval(watch_, None, frame.f_locals)

                    type_ = type(eval_result)
                    hash_ = str(id(eval_result))
                    next_id = processor.next_id()

                    watcher = Watcher(watch, watch_)

                    processor.process_variable(hash_, watch, next_id, watcher, type_, eval_result, 0)
                    processor.add_watcher(watcher)
                except Exception:
                    our_logger.exception("Error evaluating watcher %s", watch_)
        return

    def process_log_point(self, bp_log, frame):
        logger = logging.getLogger(bp_log.args['logger_name'] or 'nerdvision')

        try:
            log_msg = self.format_log(bp_log.args['log_msg'], frame.f_locals)
            logger \
                .log(level=self.as_log_int(bp_log.args['log_level'] or "INFO"),
                     msg=log_msg)
        except Exception as e:
            message = None
            if logger is not None and BreakpointService.str2bool(bp_log.args['log_on_error']):
                message = self.escape_message(bp_log.args['log_msg'])
                logger.error("[nerd.vision] Processing log message '%s' failed with error '%s'.", message, e)
                if BreakpointService.str2bool(bp_log.args['log_frame_on_error']):
                    logger.error("[nerd.vision] Variables at frame: %s", frame.f_locals)
            if BreakpointService.str2bool(bp_log.args['snapshot_on_error']):
                processor = FrameProcessor(2, 5, 100, 10)
                processor.process_back_frame_vars = False
                processor.process_frame(frame)
                self.context_service.send_event(processor.event, bp_log, [], self.session_id, log_msg=message)
            return

        self.context_service.send_log_event(BreakpointService.bp_as_map(bp_log), log_msg, self.session_id)

    @staticmethod
    def str2bool(v):
        return str(v).lower() in ("yes", "true", "t", "1")

    @staticmethod
    def as_log_int(log_level):
        return logging.getLevelName(log_level)

    @staticmethod
    def format_log(msg, f_locals):
        class format_dict(dict):
            def __missing__(self, key):
                return "{%s}" % key

        import string
        if f_locals:
            return "[nerd.vision] %s" % string.Formatter().vformat(msg, (), format_dict(f_locals))
        else:
            return "[nerd.vision] %s" % msg

    def escape_message(self, param):
        return param.replace("{", "{{").replace("}", "}}")

    @staticmethod
    def bp_as_map(bp):
        return {
            'breakpoint_id': bp.breakpoint_id,
            'workspace_id': bp.workspace_id,
            'rel_path': bp.rel_path,
            'line_no': bp.line_no,
            'condition': bp.condition,
            'src_type': bp.src_type,
            'named_watches': dict(bp.named_watchers),
            'args': dict(bp.args)
        }
