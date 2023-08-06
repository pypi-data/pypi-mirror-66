# coding=utf-8
# Copyright 2020 The Trax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Tests for convolution layers."""

from absl.testing import absltest
from trax.layers import base
from trax.layers import convolution
from trax.shapes import ShapeDtype


class ConvolutionLayerTest(absltest.TestCase):

  def test_conv(self):
    input_signature = ShapeDtype((29, 5, 5, 20))
    result_shape = base.check_shape_agreement(convolution.Conv(30, (3, 3)),
                                              input_signature)
    self.assertEqual(result_shape, (29, 3, 3, 30))

  def test_conv_rebatch(self):
    input_signature = ShapeDtype((3, 29, 5, 5, 20))
    result_shape = base.check_shape_agreement(convolution.Conv(30, (3, 3)),
                                              input_signature)
    self.assertEqual(result_shape, (3, 29, 3, 3, 30))


class CausalConvolutionTest(absltest.TestCase):

  def test_causal_conv(self):
    input_signature = ShapeDtype((29, 5, 20))
    conv = convolution.CausalConv(filters=30, kernel_width=3)
    result_shape = base.check_shape_agreement(conv, input_signature)
    self.assertEqual(result_shape, (29, 5, 30))

    # TODO(ddohan): How to test for causality? Gradient check between positions?


if __name__ == '__main__':
  absltest.main()
