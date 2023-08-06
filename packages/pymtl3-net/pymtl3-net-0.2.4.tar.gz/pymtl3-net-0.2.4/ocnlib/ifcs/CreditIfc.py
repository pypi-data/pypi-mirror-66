"""
==========================================================================
 CreditIfc.py
==========================================================================
Credit based interfaces.

Author : Yanghui Ou
  Date : June 10, 2019
"""
from ocnlib.rtl import Counter
from pymtl3 import *
from pymtl3.stdlib.ifcs import RecvIfcRTL, SendIfcRTL, enrdy_to_str
from pymtl3.stdlib.rtl.arbiters import RoundRobinArbiterEn
from pymtl3.stdlib.rtl.Encoder import Encoder
from pymtl3.stdlib.rtl.queues import BypassQueueRTL

#-------------------------------------------------------------------------
# RTL interfaces
#-------------------------------------------------------------------------

class CreditRecvIfcRTL( Interface ):

  def construct( s, MsgType, vc=1 ):
    assert vc > 1, "We only support multiple virtual channels!"

    s.en  = InPort ( Bits1   )
    s.msg = InPort ( MsgType )
    s.yum = [ OutPort( Bits1 ) for i in range( vc ) ]

    s.MsgType = MsgType
    s.vc    = vc

  def __str__( s ):
    try:
      trace_len = s.trace_len
    except AttributeError:
      s.trace_len = len( str(s.MsgType()) )
      trace_len = s.trace_len
    return "{}:{}".format(
      enrdy_to_str( s.msg, s.en, True, s.trace_len ),
      "".join( [ "$" if x else '.' for x in s.yum ] )
    )

class CreditSendIfcRTL( Interface ):

  def construct( s, MsgType, vc=1 ):
    assert vc > 1, "We only support multiple virtual channels!"

    s.en  = OutPort( Bits1   )
    s.msg = OutPort( MsgType )
    s.yum = [ InPort( Bits1 ) for _ in range( vc ) ]

    s.MsgType = MsgType
    s.vc    = vc

  def __str__( s ):
    try:
      trace_len = s.trace_len
    except AttributeError:
      s.trace_len = len( str(s.MsgType()) )
      trace_len = s.trace_len
    return "{}:{}".format(
      enrdy_to_str( s.msg, s.en, True, s.trace_len ),
      "".join( [ "$" if s.yum[i] else '.' for i in range(s.vc) ] )
    )

#-------------------------------------------------------------------------
# CL interfaces
#-------------------------------------------------------------------------

class CreditSendIfcCL( Interface ):

  def construct( s, MsgType, vc=1 ):
    assert vc > 1, "We only support multiple virtual channels!"

    s.send_msg    = CallerPort( MsgType )
    s.recv_credit = [ CalleePort() for _ in range( vc ) ]

    s.MsgType = MsgType
    s.vc    = vc

  def __str__( s ):
    return ""

class CreditRecvIfcCL( Interface ):

  def construct( s, MsgType, vc=1 ):
    assert vc > 1, "We only support multiple virtual channels!"

    s.recv_msg    = CalleePort( MsgType )
    s.send_credit = [ CallerPort() for _ in range( vc ) ]

    s.MsgType = MsgType
    s.vc    = vc

  def __str__( s ):
    return ""

#-------------------------------------------------------------------------
# CreditIfc adapters
#-------------------------------------------------------------------------

class RecvRTL2CreditSendRTL( Component ):

  def construct( s, MsgType, vc=2, credit_line=1 ):
    assert vc > 1

    # Interface

    s.recv = RecvIfcRTL( MsgType )
    s.send = CreditSendIfcRTL( MsgType, vc )

    s.MsgType = MsgType
    s.vc    = vc

    # Components

    CreditType = mk_bits( clog2(credit_line+1) )
    VcIDType   = mk_bits( clog2( vc ) if vc > 1 else 1 )

    # FIXME: use multiple buffers to avoid deadlock.
    s.buffer = BypassQueueRTL( MsgType, num_entries=1 )
    s.credit = [ Counter( CreditType, credit_line ) for _ in range( vc ) ]

    s.recv           //=  s.buffer.enq
    s.buffer.deq.ret //=  s.send.msg

    @s.update
    def up_credit_send():
      s.send.en = b1(0)
      s.buffer.deq.en = b1(0)
      if s.buffer.deq.rdy:
        for i in range( vc ):
          if VcIDType(i) == s.buffer.deq.ret.vc_id and s.credit[i].count > CreditType(0):
            s.send.en = b1(1)
            s.buffer.deq.en = b1(1)

    @s.update
    def up_counter_decr():
      for i in range( vc ):
        s.credit[i].decr = s.send.en & ( VcIDType(i) == s.send.msg.vc_id )

    for i in range( vc ):
      s.credit[i].incr       //= s.send.yum[i]
      s.credit[i].load       //= b1(0)
      s.credit[i].load_value //= CreditType(0)

  def line_trace( s ):
    return "{}({},{}){}".format(
      s.recv,
      s.buffer.line_trace(),
      ",".join( [ str(s.credit[i].count) for i in range(s.vc) ] ),
      s.send,
    )

class CreditRecvRTL2SendRTL( Component ):

  def construct( s, MsgType, vc=2, credit_line=1, QType=BypassQueueRTL ):
    assert vc > 1

    # Interface

    s.recv = CreditRecvIfcRTL( MsgType, vc )
    s.send = SendIfcRTL( MsgType )

    s.MsgType = MsgType
    s.vc    = vc

    # Components

    CreditType = mk_bits( clog2(credit_line+1) )
    ArbReqType = mk_bits( vc )
    VcIDType   = mk_bits( clog2( vc ) if vc > 1 else 1 )

    s.buffers = [ QType( MsgType, num_entries=credit_line )
                  for _ in range( vc ) ]
    s.arbiter = RoundRobinArbiterEn( nreqs=vc )
    s.encoder = Encoder( in_nbits=vc, out_nbits=clog2(vc) )

    for i in range( vc ):
      s.buffers[i].enq.msg //= s.recv.msg
      s.buffers[i].deq.rdy //= s.arbiter.reqs[i]
    s.arbiter.grants //= s.encoder.in_
    s.arbiter.en     //= s.send.en

    @s.update
    def up_enq():
      if s.recv.en:
        for i in range( vc ):
          s.buffers[i].enq.en = s.recv.msg.vc_id == VcIDType(i)
      else:
        for i in range( vc ):
          s.buffers[i].enq.en = b1(0)

    @s.update
    def up_deq_and_send():
      for i in range( vc ):
        s.buffers[i].deq.en = b1(0)

      s.send.msg = s.buffers[ s.encoder.out ].deq.ret
      if s.send.rdy & ( s.arbiter.grants > ArbReqType(0) ):
        s.send.en = b1(1)
        s.buffers[ s.encoder.out ].deq.en = b1(1)
      else:
        s.send.en = b1(0)

    @s.update
    def up_yummy():
      for i in range( vc ):
        s.recv.yum[i] = s.buffers[i].deq.en

  def line_trace( s ):
    return "{}(){}".format( s.recv, s.send )
