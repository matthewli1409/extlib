from extlib.bfx_v2 import BFXV2
from settings.settings import BFX_DETS

bfx = BFXV2(BFX_DETS['KEY'], BFX_DETS['SECRET'])
print(f'\nbfx.get_positions(): \n{bfx.get_positions()}')
print(f'\nbfx.get_aum(): {bfx.get_aum()}')
print(f'\nbfx.get_cur_pos(): {bfx.get_cur_pos()}')
