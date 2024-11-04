#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

'''Echo cancellation (template).'''

import logging

import minimal
import buffer
import math


class Echo_Cancellation(buffer.Buffering):
    def __init__(self):
        super().__init__()
        logging.info(__doc__)
        self.delay = int(math.ceil(60 / 1000 / self.chunk_time))
        logging.info(f'Delay: {self.delay}')
        self.attenuation = 1
        self.sent_chunks = []
        self.sent_chunks = [self.zero_chunk] * self.delay
        self.last_played_chunk = self.zero_chunk

    def cancel_echo(self, microphone_signal):
        if (len(self.sent_chunks) >= self.delay):
            echo_estimate = self.sent_chunks[-self.delay].flatten()
            echo_signal = microphone_signal - self.attenuation * echo_estimate
            
            return echo_signal

        return microphone_signal

    def _record_IO_and_play(self, indata, outdata, frames, time, status):
        indata_flatten = indata.flatten()
        echo_signal = self.cancel_echo(indata_flatten)
        indata[:] = echo_signal.reshape(indata.shape)
        super()._record_IO_and_play(indata, outdata, frames, time, status)
        self.sent_chunks.append(outdata)
        if len(self.sent_chunks) > self.delay:  # Limit buffer size
            self.sent_chunks.pop(0)


class Echo_Cancellation__verbose(Echo_Cancellation, buffer.Buffering__verbose):
    def __init__(self):
        super().__init__()


try:
    import argcomplete  # <tab> completion for argparse.
except ImportError:
    logging.warning("Unable to import argcomplete (optional)")

if __name__ == "__main__":
    minimal.parser.description = __doc__
    try:
        argcomplete.autocomplete(minimal.parser)
    except Exception:
        logging.warning("argcomplete not working :-/")
    minimal.args = minimal.parser.parse_known_args()[0]

    if minimal.args.show_stats or minimal.args.show_samples or minimal.args.show_spectrum:
        intercom = Echo_Cancellation__verbose()
    else:
        intercom = Echo_Cancellation()
    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
        intercom.print_final_averages()
