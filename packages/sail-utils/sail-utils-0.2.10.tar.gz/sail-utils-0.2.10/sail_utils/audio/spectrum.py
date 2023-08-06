# -*- coding: utf-8 -*-
"""
module for audio spectrum analysis
"""

import wave
import numpy as np


class FreqAnalysis:
    """
    spectrum analysis class
    """

    def __init__(self, file_name: str):
        wf = wave.open(file_name, 'rb')
        n_frames = wf.getnframes()
        self._frame_rate = wf.getframerate()
        self._duration = n_frames / self._frame_rate
        str_data = wf.readframes(n_frames)
        wave_data = np.frombuffer(str_data, dtype=np.short)
        wave_data.shape = -1, 1
        self._wave_data = wave_data.T
        wf.close()

    def spectrum(self, start_offset: int, window: int, cutoff=5000) -> tuple:
        """
        spectrum of the targeted audio segment
        :param start_offset:
        :param window:
        :param cutoff:
        :return:
        """
        total_samples = self._frame_rate * window
        start = start_offset * self._frame_rate
        df = self._frame_rate / (total_samples - 1)
        spec = np.fft.fft(self._wave_data[0][start:start + total_samples])
        max_idx = min(int(cutoff / df), int(len(spec) / 2))
        freq = np.arange(0, max_idx) * df
        return freq, spec[:max_idx]

    def __str__(self):
        return f"frame_rate: {self._frame_rate}\n" \
               f"duration: {self._duration}"
