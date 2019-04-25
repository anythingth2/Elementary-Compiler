
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftEQUALSNOT_EQUALSleftUPWARDUPWARD_EQUALSDOWNWARDDOWNWARD_EQUALSleftPLUSMINUSleftTIMESDIVIDEMODULOrightUMINUSleftL_PARENR_PARENL_ARRAYR_ARRAYASSIGNMENT BEGIN DEC DIVIDE DOWNWARD DOWNWARD_EQUALS ELSE END EQUALS ID IF INC L_ARRAY L_ELEM_ARRAY L_PAREN MINUS MODULO NEWLINE NOT_EQUALS NUMBER PLUS PRINT REPEAT R_ARRAY R_ELEM_ARRAY R_PAREN SEPARATOR STRING TIMES TO UPWARD UPWARD_EQUALSstm : ID ASSIGNMENT expr NEWLINEstm : ID ASSIGNMENT arr NEWLINEstm : ID L_ARRAY expr R_ARRAY ASSIGNMENT expr NEWLINEstm : IF cond NEWLINE BEGIN NEWLINE stm END NEWLINEstm : IF cond NEWLINE BEGIN NEWLINE stm END NEWLINE ELSE NEWLINE BEGIN NEWLINE stm END NEWLINEstm : REPEAT expr TO expr INC expr NEWLINE BEGIN NEWLINE stm END NEWLINE\n           | REPEAT expr TO expr DEC expr NEWLINE BEGIN NEWLINE stm END NEWLINEstm : PRINT str NEWLINEexpr : expr PLUS expr\n            | expr MINUS expr\n            | expr TIMES expr\n            | expr DIVIDE expr\n            | expr MODULO exprexpr : MINUS expr %prec UMINUSexpr : L_PAREN expr R_PARENexpr : NUMBERexpr : IDexpr : ID L_ARRAY expr R_ARRAYcond : cond EQUALS cond\n            | cond NOT_EQUALS cond\n            | cond UPWARD cond\n            | cond UPWARD_EQUALS cond\n            | cond DOWNWARD cond\n            | cond DOWNWARD_EQUALS condcond : exprcond : L_PAREN cond R_PARENarr : L_ARRAY expr R_ARRAYarr : L_ELEM_ARRAY elem R_ELEM_ARRAYelem : exprelem : expr SEPARATOR elemstr : expr\n           | STRINGstr : str SEPARATOR str'
    
_lr_action_items = {'ID':([0,3,4,5,6,7,10,11,15,21,22,25,26,27,28,29,30,31,32,33,34,35,39,40,43,69,70,71,73,74,88,89,96,],[2,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,2,13,13,2,2,2,]),'IF':([0,71,88,89,96,],[3,3,3,3,3,]),'REPEAT':([0,71,88,89,96,],[4,4,4,4,4,]),'PRINT':([0,71,88,89,96,],[5,5,5,5,5,]),'$end':([1,42,44,45,80,84,97,98,101,],[0,-8,-1,-2,-3,-4,-6,-7,-5,]),'ASSIGNMENT':([2,49,],[6,70,]),'L_ARRAY':([2,6,13,],[7,21,39,]),'L_PAREN':([3,4,5,6,7,10,11,15,21,22,25,26,27,28,29,30,31,32,33,34,35,39,40,43,69,70,73,74,],[10,15,15,15,15,10,15,15,15,15,10,10,10,10,10,10,15,15,15,15,15,15,15,15,15,15,15,15,]),'MINUS':([3,4,5,6,7,9,10,11,12,13,14,15,17,19,21,22,23,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,43,46,48,57,58,59,60,61,63,64,65,69,70,72,73,74,76,78,79,],[11,11,11,11,11,32,11,11,-16,-17,32,11,32,32,11,11,32,11,11,11,11,11,11,11,11,11,11,11,32,-14,11,11,32,11,32,32,-9,-10,-11,-12,-13,-15,32,32,11,11,-18,11,11,32,32,32,]),'NUMBER':([3,4,5,6,7,10,11,15,21,22,25,26,27,28,29,30,31,32,33,34,35,39,40,43,69,70,73,74,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,]),'STRING':([5,43,],[18,18,]),'L_ELEM_ARRAY':([6,],[22,]),'NEWLINE':([8,9,12,13,16,17,18,19,20,38,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,67,68,72,76,78,79,81,85,86,87,93,94,95,100,],[24,-25,-16,-17,42,-31,-32,44,45,-14,71,-19,-20,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-33,-27,-28,-18,80,82,83,84,88,89,90,96,97,98,101,]),'EQUALS':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[25,-25,-16,-17,25,-25,-14,-19,-20,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'NOT_EQUALS':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[26,-25,-16,-17,26,-25,-14,-19,-20,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'UPWARD':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[27,-25,-16,-17,27,-25,-14,27,27,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'UPWARD_EQUALS':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[28,-25,-16,-17,28,-25,-14,28,28,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'DOWNWARD':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[29,-25,-16,-17,29,-25,-14,29,29,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'DOWNWARD_EQUALS':([8,9,12,13,36,37,38,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[30,-25,-16,-17,30,-25,-14,30,30,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'R_PAREN':([9,12,13,36,37,38,41,51,52,53,54,55,56,57,58,59,60,61,62,63,72,],[-25,-16,-17,62,63,-14,63,-19,-20,-21,-22,-23,-24,-9,-10,-11,-12,-13,-26,-15,-18,]),'PLUS':([9,12,13,14,17,19,23,37,38,41,46,48,57,58,59,60,61,63,64,65,72,76,78,79,],[31,-16,-17,31,31,31,31,31,-14,31,31,31,-9,-10,-11,-12,-13,-15,31,31,-18,31,31,31,]),'TIMES':([9,12,13,14,17,19,23,37,38,41,46,48,57,58,59,60,61,63,64,65,72,76,78,79,],[33,-16,-17,33,33,33,33,33,-14,33,33,33,33,33,-11,-12,-13,-15,33,33,-18,33,33,33,]),'DIVIDE':([9,12,13,14,17,19,23,37,38,41,46,48,57,58,59,60,61,63,64,65,72,76,78,79,],[34,-16,-17,34,34,34,34,34,-14,34,34,34,34,34,-11,-12,-13,-15,34,34,-18,34,34,34,]),'MODULO':([9,12,13,14,17,19,23,37,38,41,46,48,57,58,59,60,61,63,64,65,72,76,78,79,],[35,-16,-17,35,35,35,35,35,-14,35,35,35,35,35,-11,-12,-13,-15,35,35,-18,35,35,35,]),'TO':([12,13,14,38,57,58,59,60,61,63,72,],[-16,-17,40,-14,-9,-10,-11,-12,-13,-15,-18,]),'SEPARATOR':([12,13,16,17,18,38,48,57,58,59,60,61,63,66,72,],[-16,-17,43,-31,-32,-14,69,-9,-10,-11,-12,-13,-15,43,-18,]),'R_ARRAY':([12,13,23,38,46,57,58,59,60,61,63,64,72,],[-16,-17,49,-14,67,-9,-10,-11,-12,-13,-15,72,-18,]),'R_ELEM_ARRAY':([12,13,38,47,48,57,58,59,60,61,63,72,75,],[-16,-17,-14,68,-29,-9,-10,-11,-12,-13,-15,-18,-30,]),'INC':([12,13,38,57,58,59,60,61,63,65,72,],[-16,-17,-14,-9,-10,-11,-12,-13,-15,73,-18,]),'DEC':([12,13,38,57,58,59,60,61,63,65,72,],[-16,-17,-14,-9,-10,-11,-12,-13,-15,74,-18,]),'BEGIN':([24,82,83,90,],[50,85,86,93,]),'END':([42,44,45,77,80,84,91,92,97,98,99,101,],[-8,-1,-2,81,-3,-4,94,95,-6,-7,100,-5,]),'ELSE':([84,],[87,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'stm':([0,71,88,89,96,],[1,77,91,92,99,]),'cond':([3,10,25,26,27,28,29,30,],[8,36,51,52,53,54,55,56,]),'expr':([3,4,5,6,7,10,11,15,21,22,25,26,27,28,29,30,31,32,33,34,35,39,40,43,69,70,73,74,],[9,14,17,19,23,37,38,41,46,48,9,9,9,9,9,9,57,58,59,60,61,64,65,17,48,76,78,79,]),'str':([5,43,],[16,66,]),'arr':([6,],[20,]),'elem':([22,69,],[47,75,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> stm","S'",1,None,None,None),
  ('stm -> ID ASSIGNMENT expr NEWLINE','stm',4,'p_stm_assign','cc_parser.py',23),
  ('stm -> ID ASSIGNMENT arr NEWLINE','stm',4,'p_stm_declare_arr','cc_parser.py',29),
  ('stm -> ID L_ARRAY expr R_ARRAY ASSIGNMENT expr NEWLINE','stm',7,'p_stm_assign_arr','cc_parser.py',35),
  ('stm -> IF cond NEWLINE BEGIN NEWLINE stm END NEWLINE','stm',8,'p_stm_if','cc_parser.py',52),
  ('stm -> IF cond NEWLINE BEGIN NEWLINE stm END NEWLINE ELSE NEWLINE BEGIN NEWLINE stm END NEWLINE','stm',15,'p_stm_if_else','cc_parser.py',58),
  ('stm -> REPEAT expr TO expr INC expr NEWLINE BEGIN NEWLINE stm END NEWLINE','stm',12,'p_stm_loop','cc_parser.py',64),
  ('stm -> REPEAT expr TO expr DEC expr NEWLINE BEGIN NEWLINE stm END NEWLINE','stm',12,'p_stm_loop','cc_parser.py',65),
  ('stm -> PRINT str NEWLINE','stm',3,'p_stm_print','cc_parser.py',73),
  ('expr -> expr PLUS expr','expr',3,'p_expr_op','cc_parser.py',79),
  ('expr -> expr MINUS expr','expr',3,'p_expr_op','cc_parser.py',80),
  ('expr -> expr TIMES expr','expr',3,'p_expr_op','cc_parser.py',81),
  ('expr -> expr DIVIDE expr','expr',3,'p_expr_op','cc_parser.py',82),
  ('expr -> expr MODULO expr','expr',3,'p_expr_op','cc_parser.py',83),
  ('expr -> MINUS expr','expr',2,'p_expr_uminus','cc_parser.py',88),
  ('expr -> L_PAREN expr R_PAREN','expr',3,'p_expr_group','cc_parser.py',93),
  ('expr -> NUMBER','expr',1,'p_expr_number','cc_parser.py',99),
  ('expr -> ID','expr',1,'p_expr_name','cc_parser.py',104),
  ('expr -> ID L_ARRAY expr R_ARRAY','expr',4,'p_expr_name_arr','cc_parser.py',113),
  ('cond -> cond EQUALS cond','cond',3,'p_cond_op','cc_parser.py',126),
  ('cond -> cond NOT_EQUALS cond','cond',3,'p_cond_op','cc_parser.py',127),
  ('cond -> cond UPWARD cond','cond',3,'p_cond_op','cc_parser.py',128),
  ('cond -> cond UPWARD_EQUALS cond','cond',3,'p_cond_op','cc_parser.py',129),
  ('cond -> cond DOWNWARD cond','cond',3,'p_cond_op','cc_parser.py',130),
  ('cond -> cond DOWNWARD_EQUALS cond','cond',3,'p_cond_op','cc_parser.py',131),
  ('cond -> expr','cond',1,'p_cond_expr','cc_parser.py',136),
  ('cond -> L_PAREN cond R_PAREN','cond',3,'p_cond_group','cc_parser.py',141),
  ('arr -> L_ARRAY expr R_ARRAY','arr',3,'p_arr_size','cc_parser.py',148),
  ('arr -> L_ELEM_ARRAY elem R_ELEM_ARRAY','arr',3,'p_arr_elem','cc_parser.py',153),
  ('elem -> expr','elem',1,'p_elem','cc_parser.py',159),
  ('elem -> expr SEPARATOR elem','elem',3,'p_elem_many','cc_parser.py',164),
  ('str -> expr','str',1,'p_str','cc_parser.py',170),
  ('str -> STRING','str',1,'p_str','cc_parser.py',171),
  ('str -> str SEPARATOR str','str',3,'p_str_many','cc_parser.py',176),
]
