"""Mimc hash function."""
"""
This module adapted from https://github.com/OlegJakushkin/deepblockchains/blob/master/vdf/mimc/python/mimc.py by Sourabh Niyogi https://github.com/sourabhniyogi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
modulus = 2**256 - 2**32 * 351 + 1
little_fermat_expt = (modulus*2-1)//3
round_constants = [(i**7) ^ 42 for i in range(64)]


def forward_mimc(inp: int, steps: int) -> int:
    for i in range(1,steps):
        inp = (inp**3 + round_constants[i % len(round_constants)]) % modulus
    return inp


def reverse_mimc(input_data: int, steps: int) -> int:
    rtrace = input_data

    for i in range(steps - 1, 0, -1):
        rtrace = pow(rtrace-round_constants[i%len(round_constants)],
                     little_fermat_expt, modulus)
    return rtrace

