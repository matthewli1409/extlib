from extlib.bfx_v2 import BFXV2
from config.settings import BFX_DETS

bfx = BFXV2(BFX_DETS['KEY'], BFX_DETS['SECRET'])
print(bfx.get_positions())
