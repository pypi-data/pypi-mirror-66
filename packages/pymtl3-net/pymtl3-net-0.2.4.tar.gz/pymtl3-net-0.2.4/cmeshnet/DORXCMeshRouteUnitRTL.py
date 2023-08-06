"""
=========================================================================
DORXRouteUnitRTL.py
=========================================================================
A DOR-X route unit with get/give interface for CMesh.

Author : Yanghui Ou, Cheng Tan
  Date : Mar 25, 2019
"""
from pymtl3 import *
from pymtl3.stdlib.ifcs import GetIfcRTL, GiveIfcRTL

from .directions import *


class DORXCMeshRouteUnitRTL( Component ):

  def construct( s, PacketType, PositionType, num_outports = 8 ):

    # Constants

    s.num_outports = num_outports
    TType = mk_bits( num_outports )

    # Interface

    s.get  = GetIfcRTL( PacketType )
    s.give = [ GiveIfcRTL (PacketType) for _ in range ( s.num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.give_ens = Wire( mk_bits( s.num_outports ) )
    s.give_rdy = [ Wire( Bits1 ) for _ in range( s.num_outports )]

    # Connections

    for i in range( s.num_outports ):
      s.get.ret     //= s.give[i].ret
      s.give_ens[i] //= s.give[i].en
      s.give_rdy[i] //= s.give[i].rdy

    # Routing logic

    @s.update
    def up_ru_routing():

      s.out_dir = 0
      for i in range( s.num_outports ):
        s.give_rdy[i] = Bits1(0)

      if s.get.rdy:
        if s.pos.pos_x == s.get.ret.dst_x and s.pos.pos_y == s.get.ret.dst_y:
          s.give_rdy[ Bits3( 4 ) + s.get.ret.dst_ter ] = Bits1(1)
        elif s.get.ret.dst_x < s.pos.pos_x:
          s.give_rdy[2] = Bits1(1)
        elif s.get.ret.dst_x > s.pos.pos_x:
          s.give_rdy[3] = Bits1(1)
        elif s.get.ret.dst_y < s.pos.pos_y:
          s.give_rdy[1] = Bits1(1)
        else:
          s.give_rdy[0] = Bits1(1)

    @s.update
    def up_ru_get_en():
      s.get.en = s.give_ens > TType(0)

  # Line trace

  def line_trace( s ):
    out_str = "".join([ f"{s.give[i]}" for i in range( s.num_outports ) ])
    return f"{s.get}(){out_str}"
