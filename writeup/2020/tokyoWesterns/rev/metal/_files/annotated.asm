.version 3.6
.kernel "encrypt"


// .decl null v_type=G v_name=null
// .decl thread_x v_type=G v_name=thread_x
// .decl thread_y v_type=G v_name=thread_y
// .decl group_id_x v_type=G v_name=group_id_x
// .decl group_id_y v_type=G v_name=group_id_y
// .decl group_id_z v_type=G v_name=group_id_z
// .decl tsc v_type=G v_name=tsc
// .decl r0 v_type=G v_name=r0
// .decl arg v_type=G v_name=arg
// .decl retval v_type=G v_name=retval
// .decl sp v_type=G v_name=sp
// .decl fp v_type=G v_name=fp
// .decl hw_id v_type=G v_name=hw_id
// .decl sr0 v_type=G v_name=sr0
// .decl cr0 v_type=G v_name=cr0
// .decl ce0 v_type=G v_name=ce0
// .decl dbg0 v_type=G v_name=dbg0
// .decl color v_type=G v_name=color
// .decl T0 v_type=T v_name=T0
// .decl T1 v_type=T v_name=T1
// .decl T2 v_type=T v_name=T2
// .decl TSS v_type=T v_name=TSS
// .decl T252 v_type=T v_name=T252
// .decl T255 v_type=T v_name=T255

.decl V32 v_type=G type=uw num_elts=1 align=word
.decl V33 v_type=G type=d num_elts=1 align=dword
.decl V34 v_type=G type=df num_elts=64 align=GRF
.decl V35 v_type=G type=d num_elts=1 align=dword
.decl V36 v_type=G type=d num_elts=1 align=dword
.decl V37 v_type=G type=d num_elts=1 align=dword
.decl V38 v_type=G type=ud num_elts=1 align=dword
.decl V39 v_type=G type=uq num_elts=8 align=GRF
.decl V40 v_type=G type=w num_elts=1 align=word
.decl V41 v_type=G type=d num_elts=1 align=dword
.decl V42 v_type=G type=w num_elts=1 align=word
.decl V43 v_type=G type=df num_elts=1 align=qword
.decl V44 v_type=G type=w num_elts=1 align=word
.decl V45 v_type=G type=d num_elts=4 align=dword
.decl V46 v_type=G type=d num_elts=1 align=dword
.decl V47 v_type=G type=w num_elts=1 align=word
.decl V48 v_type=G type=w num_elts=1 align=word
.decl V49 v_type=G type=d num_elts=1 align=dword
.decl V50 v_type=G type=d num_elts=4 align=dword
.decl V51 v_type=G type=b num_elts=4 align=dword
.decl V52 v_type=G type=w num_elts=1 align=word
.decl V53 v_type=G type=w num_elts=1 align=word
.decl V54 v_type=G type=w num_elts=1 align=word
.decl V55 v_type=G type=w num_elts=1 align=word
.decl V56 v_type=G type=w num_elts=1 align=word
.decl V57 v_type=G type=df num_elts=1 align=qword
.decl V58 v_type=G type=df num_elts=64 align=GRF
.decl V59 v_type=G type=d num_elts=1 align=dword
.decl V60 v_type=G type=w num_elts=1 align=word
.decl V61 v_type=G type=d num_elts=1 align=dword
.decl V62 v_type=G type=w num_elts=1 align=word
.decl V63 v_type=G type=w num_elts=1 align=word
.decl V64 v_type=G type=d num_elts=1 align=dword
.decl V65 v_type=G type=w num_elts=1 align=word
.decl V66 v_type=G type=df num_elts=64 align=GRF
.decl V67 v_type=G type=d num_elts=8 align=GRF
.decl V68 v_type=G type=d num_elts=1 align=dword
.decl V69 v_type=G type=d num_elts=1 align=dword
.decl V70 v_type=G type=d num_elts=1 align=dword
.decl V71 v_type=G type=w num_elts=1 align=word
.decl V72 v_type=G type=w num_elts=1 align=word
.decl V73 v_type=G type=w num_elts=1 align=word
.decl V74 v_type=G type=w num_elts=1 align=word
.decl V75 v_type=G type=df num_elts=1 align=qword
.decl V76 v_type=G type=w num_elts=1 align=word
.decl V77 v_type=G type=df num_elts=1 align=qword
.decl V78 v_type=G type=w num_elts=1 align=word
.decl V79 v_type=G type=df num_elts=1 align=qword
.decl V80 v_type=G type=df num_elts=8 align=GRF
.decl V81 v_type=G type=d num_elts=1 align=dword
.decl V82 v_type=G type=w num_elts=1 align=word
.decl V83 v_type=G type=w num_elts=1 align=word
.decl V84 v_type=G type=df num_elts=8 align=GRF
.decl V85 v_type=G type=d num_elts=1 align=dword
.decl V86 v_type=G type=w num_elts=1 align=word
.decl V87 v_type=G type=df num_elts=64 align=GRF
.decl V88 v_type=G type=d num_elts=1 align=dword
.decl V89 v_type=G type=d num_elts=1 align=dword
.decl V90 v_type=G type=d num_elts=1 align=dword
.decl V91 v_type=G type=d num_elts=1 align=dword
.decl V92 v_type=G type=w num_elts=1 align=word
.decl V93 v_type=G type=d num_elts=49 align=GRF
.decl V94 v_type=G type=d num_elts=49 align=GRF
.decl V95 v_type=G type=w num_elts=16 align=GRF
.decl V96 v_type=G type=w num_elts=1 align=word
.decl V97 v_type=G type=w num_elts=16 align=GRF
.decl V98 v_type=G type=w num_elts=1 align=word
.decl V99 v_type=G type=w num_elts=1 align=word
.decl V100 v_type=G type=w num_elts=16 align=GRF
.decl V101 v_type=G type=w num_elts=1 align=word
.decl V102 v_type=G type=w num_elts=32 align=GRF
.decl V103 v_type=G type=w num_elts=16 align=GRF
.decl V104 v_type=G type=w num_elts=1 align=word
.decl V105 v_type=G type=df num_elts=49 align=GRF
.decl V106 v_type=G type=d num_elts=1 align=dword
.decl V107 v_type=G type=w num_elts=1 align=word
.decl V108 v_type=G type=w num_elts=1 align=word
.decl V109 v_type=G type=d num_elts=1 align=dword
.decl V110 v_type=G type=w num_elts=1 align=word
.decl V111 v_type=G type=w num_elts=1 align=word
.decl V112 v_type=G type=w num_elts=1 align=word
.decl V113 v_type=G type=w num_elts=1 align=word
.decl V114 v_type=G type=w num_elts=1 align=word
.decl V115 v_type=G type=d num_elts=1 align=dword
.decl V116 v_type=G type=d num_elts=1 align=dword
.decl V117 v_type=G type=w num_elts=1 align=word
.decl V118 v_type=G type=d num_elts=1 align=dword
.decl V119 v_type=G type=w num_elts=1 align=word
.decl V120 v_type=G type=w num_elts=1 align=word
.decl V121 v_type=G type=w num_elts=1 align=word
.decl V122 v_type=G type=w num_elts=1 align=word
.decl V123 v_type=G type=df num_elts=1 align=qword
.decl V124 v_type=G type=w num_elts=1 align=word
.decl V125 v_type=G type=df num_elts=1 align=qword
.decl V126 v_type=G type=w num_elts=1 align=word
.decl V127 v_type=G type=d num_elts=1 align=dword
.decl V128 v_type=G type=w num_elts=1 align=word
.decl V129 v_type=G type=w num_elts=1 align=word
.decl V130 v_type=G type=df num_elts=8 align=GRF
.decl V131 v_type=G type=d num_elts=1 align=dword
.decl V132 v_type=G type=d num_elts=1 align=dword
.decl V133 v_type=G type=w num_elts=1 align=word
.decl V134 v_type=G type=w num_elts=2 align=dword
.decl V135 v_type=G type=w num_elts=1 align=word
.decl V136 v_type=G type=d num_elts=1 align=dword
.decl V137 v_type=G type=d num_elts=1 align=dword
.decl V138 v_type=G type=uw num_elts=2 align=dword
.decl V139 v_type=G type=ub num_elts=16 align=GRF
.decl V140 v_type=G type=ud num_elts=1 align=dword
.decl V141 v_type=G type=d num_elts=1 align=dword
.decl V142 v_type=G type=d num_elts=1 align=dword
.decl V143 v_type=G type=uw num_elts=2 align=dword
.decl V144 v_type=G type=ub num_elts=16 align=GRF
.decl V145 v_type=G type=ud num_elts=1 align=dword
.decl V146 v_type=G type=d num_elts=1 align=dword
.decl V147 v_type=G type=d num_elts=1 align=dword
.decl V148 v_type=G type=ub num_elts=64 align=GRF
.decl V149 v_type=G type=d num_elts=1 align=dword
.decl V150 v_type=G type=d num_elts=1 align=dword
.decl V151 v_type=G type=w num_elts=1 align=word
.decl V152 v_type=G type=d num_elts=1 align=dword
.decl V153 v_type=G type=uw num_elts=2 align=dword
.decl V154 v_type=G type=w num_elts=1 align=word
.decl V155 v_type=G type=w num_elts=1 align=word
.decl V156 v_type=G type=ub num_elts=512 align=GRF
.decl V157 v_type=G type=d num_elts=1 align=dword
.decl V158 v_type=G type=w num_elts=1 align=word
.decl V159 v_type=G type=ub num_elts=8 align=qword
.decl V160 v_type=G type=ub num_elts=8 align=qword
.decl V161 v_type=G type=ub num_elts=8 align=qword
.decl V162 v_type=G type=ub num_elts=8 align=qword
.decl V163 v_type=G type=ub num_elts=8 align=qword
.decl V164 v_type=G type=ub num_elts=8 align=qword
.decl V165 v_type=G type=ub num_elts=8 align=qword
.decl V166 v_type=G type=w num_elts=1 align=word
.decl V167 v_type=G type=df num_elts=1 align=qword
.decl V168 v_type=G type=df num_elts=1 align=qword
.decl V169 v_type=G type=d num_elts=1 align=dword
.decl V170 v_type=G type=w num_elts=1 align=word
.decl V171 v_type=G type=w num_elts=1 align=word
.decl V172 v_type=G type=w num_elts=1 align=word
.decl V173 v_type=G type=w num_elts=1 align=word
.decl V174 v_type=G type=df num_elts=1 align=qword
.decl V175 v_type=G type=d num_elts=1 align=dword
.decl V176 v_type=G type=d num_elts=1 align=dword
.decl V177 v_type=G type=df num_elts=1 align=qword
.decl V178 v_type=G type=w num_elts=1 align=word
.decl V179 v_type=G type=w num_elts=1 align=word
.decl V180 v_type=G type=w num_elts=1 align=word
.decl V181 v_type=G type=df num_elts=1 align=qword
.decl V182 v_type=G type=w num_elts=1 align=word
.decl V183 v_type=G type=w num_elts=1 align=word
.decl V184 v_type=G type=df num_elts=1 align=qword
.decl V185 v_type=G type=df num_elts=1 align=qword
.decl V186 v_type=G type=df num_elts=1 align=qword
.decl V187 v_type=G type=df num_elts=1 align=qword
.decl V188 v_type=G type=d num_elts=1 align=dword
.decl V189 v_type=G type=d num_elts=1 align=dword
.decl V190 v_type=G type=df num_elts=1 align=qword
.decl V191 v_type=G type=df num_elts=1 align=qword
.decl V192 v_type=G type=w num_elts=1 align=word
.decl V193 v_type=G type=w num_elts=1 align=word
.decl V194 v_type=G type=w num_elts=1 align=word
.decl V195 v_type=G type=w num_elts=1 align=word
.decl V196 v_type=G type=w num_elts=1 align=word
.decl V197 v_type=G type=df num_elts=1 align=qword
.decl V198 v_type=G type=w num_elts=1 align=word
.decl V199 v_type=G type=w num_elts=1 align=word
.decl V200 v_type=G type=df num_elts=1 align=qword
.decl V201 v_type=G type=w num_elts=1 align=word
.decl V202 v_type=G type=w num_elts=1 align=word
.decl V203 v_type=G type=w num_elts=1 align=word
.decl V204 v_type=G type=d num_elts=1 align=dword
.decl V205 v_type=G type=w num_elts=1 align=word
.decl V206 v_type=G type=w num_elts=1 align=word
.decl V207 v_type=G type=w num_elts=1 align=word
.decl V208 v_type=G type=w num_elts=1 align=word
.decl V209 v_type=G type=w num_elts=1 align=word
.decl V210 v_type=G type=df num_elts=1 align=qword
.decl V211 v_type=G type=w num_elts=1 align=word
.decl V212 v_type=G type=w num_elts=1 align=word
.decl V213 v_type=G type=df num_elts=1 align=qword
.decl V214 v_type=G type=w num_elts=1 align=word
.decl V215 v_type=G type=df num_elts=1 align=qword
.decl V216 v_type=G type=w num_elts=1 align=word
.decl V217 v_type=G type=w num_elts=1 align=word
.decl V218 v_type=G type=df num_elts=1 align=qword
.decl V219 v_type=G type=d num_elts=1 align=dword
.decl V220 v_type=G type=w num_elts=1 align=word
.decl V221 v_type=G type=w num_elts=1 align=word
.decl V222 v_type=G type=w num_elts=1 align=word
.decl V223 v_type=G type=w num_elts=1 align=word
.decl V224 v_type=G type=df num_elts=1 align=qword
.decl V225 v_type=G type=w num_elts=1 align=word
.decl V226 v_type=G type=w num_elts=1 align=word
.decl V227 v_type=G type=df num_elts=1 align=qword
.decl V228 v_type=G type=d num_elts=1 align=dword
.decl V229 v_type=G type=w num_elts=1 align=word
.decl V230 v_type=G type=w num_elts=1 align=word
.decl V231 v_type=G type=w num_elts=1 align=word
.decl V232 v_type=G type=w num_elts=1 align=word
.decl V233 v_type=G type=df num_elts=1 align=qword
.decl V234 v_type=G type=w num_elts=1 align=word
.decl V235 v_type=G type=w num_elts=1 align=word
.decl V236 v_type=G type=df num_elts=1 align=qword
.decl V237 v_type=G type=d num_elts=1 align=dword
.decl V238 v_type=G type=w num_elts=1 align=word
.decl V239 v_type=G type=d num_elts=1 align=dword
.decl V240 v_type=G type=w num_elts=1 align=word
.decl V241 v_type=G type=w num_elts=1 align=word
.decl V242 v_type=G type=df num_elts=1 align=qword
.decl V243 v_type=G type=w num_elts=1 align=word
.decl V244 v_type=G type=w num_elts=1 align=word
.decl V245 v_type=G type=w num_elts=1 align=word
.decl V246 v_type=G type=df num_elts=1 align=qword
.decl V247 v_type=G type=w num_elts=1 align=word
.decl V248 v_type=G type=df num_elts=1 align=qword
.decl V249 v_type=G type=w num_elts=1 align=word
.decl V250 v_type=G type=w num_elts=1 align=word
.decl V251 v_type=G type=df num_elts=1 align=qword
.decl V252 v_type=G type=d num_elts=1 align=dword
.decl V253 v_type=G type=w num_elts=1 align=word
.decl V254 v_type=G type=w num_elts=1 align=word
.decl V255 v_type=G type=w num_elts=1 align=word
.decl V256 v_type=G type=df num_elts=1 align=qword
.decl V257 v_type=G type=w num_elts=1 align=word
.decl V258 v_type=G type=w num_elts=1 align=word
.decl V259 v_type=G type=df num_elts=1 align=qword
.decl V260 v_type=G type=w num_elts=1 align=word
.decl V261 v_type=G type=df num_elts=1 align=qword
.decl V262 v_type=G type=w num_elts=1 align=word
.decl V263 v_type=G type=w num_elts=1 align=word
.decl V264 v_type=G type=df num_elts=1 align=qword
.decl V265 v_type=G type=d num_elts=1 align=dword
.decl V266 v_type=G type=w num_elts=1 align=word
.decl V267 v_type=G type=w num_elts=1 align=word
.decl V268 v_type=G type=df num_elts=1 align=qword
.decl V269 v_type=G type=w num_elts=1 align=word
.decl V270 v_type=G type=w num_elts=1 align=word
.decl V271 v_type=G type=df num_elts=1 align=qword
.decl V272 v_type=G type=d num_elts=1 align=dword
.decl V273 v_type=G type=w num_elts=1 align=word
.decl V274 v_type=G type=w num_elts=1 align=word
.decl V275 v_type=G type=w num_elts=1 align=word
.decl V276 v_type=G type=d num_elts=1 align=dword
.decl V277 v_type=G type=w num_elts=1 align=word
.decl V278 v_type=G type=w num_elts=1 align=word
.decl V279 v_type=G type=df num_elts=1 align=qword
.decl V280 v_type=G type=w num_elts=1 align=word
.decl V281 v_type=G type=w num_elts=1 align=word
.decl V282 v_type=G type=df num_elts=1 align=qword
.decl V283 v_type=G type=df num_elts=1 align=qword
.decl V284 v_type=G type=df num_elts=1 align=qword
.decl V285 v_type=G type=d num_elts=1 align=dword
.decl V286 v_type=G type=d num_elts=1 align=dword
.decl V287 v_type=G type=df num_elts=64 align=GRF
.decl V288 v_type=G type=w num_elts=1 align=word
.decl V289 v_type=G type=d num_elts=1 align=dword
.decl V290 v_type=G type=w num_elts=1 align=word
.decl V291 v_type=G type=w num_elts=1 align=word
.decl V292 v_type=G type=df num_elts=1 align=qword
.decl V293 v_type=G type=w num_elts=1 align=word
.decl V294 v_type=G type=w num_elts=1 align=word
.decl V295 v_type=G type=df num_elts=1 align=qword
.decl V296 v_type=G type=d num_elts=1 align=dword
.decl V37.(ud[1]) v_type=G type=ud num_elts=1 align=dword alias=<V37, 0>
.decl V35.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V35, 0>
.decl V41.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V41, 0>
.decl V42.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V42, 0>
.decl V44.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V44, 0>
.decl V46.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V46, 0>
.decl V51.(d[1]) v_type=G type=d num_elts=1 align=dword alias=<V51, 0>
.decl V49.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V49, 0>
.decl V53.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V53, 0>
.decl V55.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V55, 0>
.decl V56.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V56, 0>
.decl V59.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V59, 0>
.decl V61.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V61, 0>
.decl V63.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V63, 0>
.decl V64.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V64, 0>
.decl V65.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V65, 0>
.decl V70.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V70, 0>
.decl V71.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V71, 0>
.decl V69.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V69, 0>
.decl V74.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V74, 0>
.decl V76.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V76, 0>
.decl V78.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V78, 0>
.decl V81.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V81, 0>
.decl V83.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V83, 0>
.decl V82.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V82, 0>
.decl V85.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V85, 0>
.decl V86.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V86, 0>
.decl V91.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V91, 0>
.decl V92.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V92, 0>
.decl V93.(w[98]) v_type=G type=w num_elts=98 align=GRF alias=<V93, 0>
.decl V94.(w[98]) v_type=G type=w num_elts=98 align=GRF alias=<V94, 0>
.decl V102.(uw[32]) v_type=G type=uw num_elts=32 align=GRF alias=<V102, 0>
.decl V103.(uw[16]) v_type=G type=uw num_elts=16 align=GRF alias=<V103, 0>
.decl V104.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V104, 0>
.decl V106.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V106, 0>
.decl V109.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V109, 0>
.decl V112.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V112, 0>
.decl V113.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V113, 0>
.decl V114.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V114, 0>
.decl V116.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V116, 0>
.decl V117.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V117, 0>
.decl V119.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V119, 0>
.decl V122.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V122, 0>
.decl V124.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V124, 0>
.decl V126.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V126, 0>
.decl V127.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V127, 0>
.decl V129.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V129, 0>
.decl V128.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V128, 0>
.decl V132.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V132, 0>
.decl V133.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V133, 0>
.decl V134.(d[1]) v_type=G type=d num_elts=1 align=dword alias=<V134, 0>
.decl V135.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V135, 0>
.decl V156.(d[128]) v_type=G type=d num_elts=128 align=GRF alias=<V156, 0>
.decl V138.(d[1]) v_type=G type=d num_elts=1 align=dword alias=<V138, 0>
.decl V137.(ud[1]) v_type=G type=ud num_elts=1 align=dword alias=<V137, 0>
.decl V143.(d[1]) v_type=G type=d num_elts=1 align=dword alias=<V143, 0>
.decl V142.(ud[1]) v_type=G type=ud num_elts=1 align=dword alias=<V142, 0>
.decl V147.(ud[1]) v_type=G type=ud num_elts=1 align=dword alias=<V147, 0>
.decl V149.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V149, 0>
.decl V153.(d[1]) v_type=G type=d num_elts=1 align=dword alias=<V153, 0>
.decl V152.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V152, 0>
.decl V155.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V155, 0>
.decl V157.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V157, 0>
.decl V158.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V158, 0>
.decl V159.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V159, 0>
.decl V160.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V160, 0>
.decl V161.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V161, 0>
.decl V162.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V162, 0>
.decl V163.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V163, 0>
.decl V164.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V164, 0>
.decl V165.(uq[1]) v_type=G type=uq num_elts=1 align=qword alias=<V165, 0>
.decl V67.(w[16]) v_type=G type=w num_elts=16 align=GRF alias=<V67, 0>
.decl V166.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V166, 0>
.decl V169.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V169, 0>
.decl V170.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V170, 0>
.decl V173.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V173, 0>
.decl V176.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V176, 0>
.decl V178.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V178, 0>
.decl V175.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V175, 0>
.decl V180.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V180, 0>
.decl V183.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V183, 0>
.decl V188.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V188, 0>
.decl V189.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V189, 0>
.decl V196.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V196, 0>
.decl V198.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V198, 0>
.decl V199.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V199, 0>
.decl V202.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V202, 0>
.decl V203.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V203, 0>
.decl V204.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V204, 0>
.decl V208.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V208, 0>
.decl V209.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V209, 0>
.decl V212.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V212, 0>
.decl V214.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V214, 0>
.decl V217.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V217, 0>
.decl V219.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V219, 0>
.decl V221.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V221, 0>
.decl V223.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V223, 0>
.decl V226.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V226, 0>
.decl V228.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V228, 0>
.decl V230.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V230, 0>
.decl V232.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V232, 0>
.decl V235.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V235, 0>
.decl V238.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V238, 0>
.decl V239.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V239, 0>
.decl V241.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V241, 0>
.decl V245.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V245, 0>
.decl V247.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V247, 0>
.decl V250.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V250, 0>
.decl V252.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V252, 0>
.decl V255.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V255, 0>
.decl V258.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V258, 0>
.decl V260.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V260, 0>
.decl V263.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V263, 0>
.decl V265.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V265, 0>
.decl V267.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V267, 0>
.decl V270.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V270, 0>
.decl V273.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V273, 0>
.decl V276.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V276, 0>
.decl V278.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V278, 0>
.decl V281.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V281, 0>
.decl V285.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V285, 0>
.decl V289.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V289, 0>
.decl V291.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V291, 0>
.decl V286.(w[2]) v_type=G type=w num_elts=2 align=dword alias=<V286, 0>
.decl V294.(uw[1]) v_type=G type=uw num_elts=1 align=word alias=<V294, 0>
.decl A0 v_type=A num_elts=1
.decl A1 v_type=A num_elts=1
.decl A2 v_type=A num_elts=1
.decl A3 v_type=A num_elts=1
.decl A4 v_type=A num_elts=1
.decl A5 v_type=A num_elts=1
.decl A6 v_type=A num_elts=1
.decl A7 v_type=A num_elts=1
.decl A8 v_type=A num_elts=1
.decl A9 v_type=A num_elts=1
.decl A10 v_type=A num_elts=1
.decl A11 v_type=A num_elts=1
.decl A12 v_type=A num_elts=1
.decl A13 v_type=A num_elts=1
.decl A14 v_type=A num_elts=1
.decl A15 v_type=A num_elts=1
.decl A16 v_type=A num_elts=1
.decl A17 v_type=A num_elts=8
.decl A18 v_type=A num_elts=8
.decl A19 v_type=A num_elts=8
.decl A20 v_type=A num_elts=8
.decl A21 v_type=A num_elts=16
.decl A22 v_type=A num_elts=1
.decl A23 v_type=A num_elts=1
.decl A24 v_type=A num_elts=1
.decl A25 v_type=A num_elts=1
.decl A26 v_type=A num_elts=1
.decl A27 v_type=A num_elts=1
.decl A28 v_type=A num_elts=1
.decl A29 v_type=A num_elts=1
.decl A30 v_type=A num_elts=1
.decl A31 v_type=A num_elts=1
.decl A32 v_type=A num_elts=1
.decl A33 v_type=A num_elts=1
.decl A34 v_type=A num_elts=1
.decl A35 v_type=A num_elts=1
.decl A36 v_type=A num_elts=1
.decl A37 v_type=A num_elts=1
.decl A38 v_type=A num_elts=1
.decl A39 v_type=A num_elts=1
.decl A40 v_type=A num_elts=1
.decl A41 v_type=A num_elts=1
.decl A42 v_type=A num_elts=1
.decl A43 v_type=A num_elts=1
.decl A44 v_type=A num_elts=1
.decl A45 v_type=A num_elts=1
.decl A46 v_type=A num_elts=1
.decl A47 v_type=A num_elts=1
.decl A48 v_type=A num_elts=1
.decl A49 v_type=A num_elts=1
.decl A50 v_type=A num_elts=1
.decl A51 v_type=A num_elts=1
.decl A52 v_type=A num_elts=1
.decl A53 v_type=A num_elts=1
.decl A54 v_type=A num_elts=1
.decl A55 v_type=A num_elts=1
.decl A56 v_type=A num_elts=1
.decl A57 v_type=A num_elts=1
.decl A58 v_type=A num_elts=1
.decl A59 v_type=A num_elts=1
.decl A60 v_type=A num_elts=1
.decl A61 v_type=A num_elts=1
.decl A62 v_type=A num_elts=1
.decl A63 v_type=A num_elts=1
.decl A64 v_type=A num_elts=1
.decl A65 v_type=A num_elts=1
.decl A66 v_type=A num_elts=1
.decl A67 v_type=A num_elts=1
.decl A68 v_type=A num_elts=1
.decl A69 v_type=A num_elts=1
.decl A70 v_type=A num_elts=1
.decl A71 v_type=A num_elts=1
.decl A72 v_type=A num_elts=1
.decl A73 v_type=A num_elts=1
.decl A74 v_type=A num_elts=1
.decl A75 v_type=A num_elts=1
.decl A76 v_type=A num_elts=1
.decl A77 v_type=A num_elts=1
.decl A78 v_type=A num_elts=1
.decl A79 v_type=A num_elts=1
.decl P1 v_type=P num_elts=1
.decl P2 v_type=P num_elts=1
.decl P3 v_type=P num_elts=1
.decl P4 v_type=P num_elts=1
.decl P5 v_type=P num_elts=1
.decl P6 v_type=P num_elts=1
.decl P7 v_type=P num_elts=1
.decl P8 v_type=P num_elts=1
.decl P9 v_type=P num_elts=1
.decl P10 v_type=P num_elts=1
.decl P11 v_type=P num_elts=1
.decl P12 v_type=P num_elts=1
.decl P13 v_type=P num_elts=1
.decl P14 v_type=P num_elts=1
.decl P15 v_type=P num_elts=1
.decl P16 v_type=P num_elts=1
.decl P17 v_type=P num_elts=1
.decl P18 v_type=P num_elts=1
.decl P19 v_type=P num_elts=1
.decl P20 v_type=P num_elts=1
.decl P21 v_type=P num_elts=1
.decl P22 v_type=P num_elts=1
.decl P23 v_type=P num_elts=1
.decl P24 v_type=P num_elts=1
.decl P25 v_type=P num_elts=1
.decl P26 v_type=P num_elts=1
.decl P27 v_type=P num_elts=1
.decl P28 v_type=P num_elts=1
.decl P29 v_type=P num_elts=1
.decl P30 v_type=P num_elts=1
.decl P31 v_type=P num_elts=1
.decl P32 v_type=P num_elts=1
.decl P33 v_type=P num_elts=1
.decl P34 v_type=P num_elts=1
.decl P35 v_type=P num_elts=1
.decl P36 v_type=P num_elts=1
.decl P37 v_type=P num_elts=1
.decl P38 v_type=P num_elts=1
.decl P39 v_type=P num_elts=1
.decl P40 v_type=P num_elts=1
.decl P41 v_type=P num_elts=1
.decl P42 v_type=P num_elts=1
.decl P43 v_type=P num_elts=1
.decl P44 v_type=P num_elts=1
.decl P45 v_type=P num_elts=1
.decl P46 v_type=P num_elts=1
.decl P47 v_type=P num_elts=1
.decl P48 v_type=P num_elts=1
.decl P49 v_type=P num_elts=1
.decl P50 v_type=P num_elts=1
.decl P51 v_type=P num_elts=1
.decl P52 v_type=P num_elts=1
.decl P53 v_type=P num_elts=1
.decl P54 v_type=P num_elts=1
.decl P55 v_type=P num_elts=1
.decl P56 v_type=P num_elts=1
.decl P57 v_type=P num_elts=1
.decl P58 v_type=P num_elts=1
.decl P59 v_type=P num_elts=1
.decl P60 v_type=P num_elts=1
.decl P61 v_type=P num_elts=1
.decl P62 v_type=P num_elts=1
.decl T6 v_type=T num_elts=1 v_name=T6
.decl T7 v_type=T num_elts=1 v_name=T7
.decl T8 v_type=T num_elts=1 v_name=T8
.input T8 offset=32 size=4
.input T6 offset=36 size=4
.input T7 offset=40 size=4
.kernel_attr AsmName="metal_genx_0.asm"
.kernel_attr NoBarrier=

.function "encrypt_BB_0_1_0"

encrypt_BB_0_1_0:
    // v32 = thread_y
    // v33 = thread_y
    mov<1>               V32:uw               thread_y:G          
    mov<1>               V33:d                V32:uw

    // v34[:8] = 0
    mov<8>               V34[0:]:df           0x0:df

    // v146 = thread_y
    mov<1>               V146:d               V33:d

    // v34 = func_getDataMatrixId(thread_y)
    call<1>              func_getDataMatrixId

    mov<1>               V35:d                0x0:d

    // v58 = [None] * 64
    lifetime.start       V58                 

BB_2_3:
    // for v35 in range(0, 8):
        // v38 = thread_y * 32 + v35 * 4
        // v38p = thread_y * 64 + v35 * 8
        shl<1>               V36:d                V35:d                0x6:d               
        mov<1>               V37:d                0x200:d             
        mad<1>               V37:d                V32:uw               V37:d                V36:d               
        shr<1>               V38:ud               V37.(ud[1]):ud       0x4:ud

        // v39 = inp_t6[v38p:v38p+8]
        oword_ld             (4)                  T6                   V38(0,0)<0;1,0>      V39.0

        // v40 = v35 * 8 * 8
        shl<1>               V40:w                V35.(w[2])[0]:w      0x6:w               
        mov<1>               V41:d                0x0:d               

BB_3_4:
        // for v41 in range(0, 8):
            // v43 = v39[v41]
            shl<1>               V42:w                V41.(w[2])[0]:w      0x3:w
            addr_add<1>          A0[0:1]:A            &V39+0               V42.(uw[1]):uw      
            mov<1>               V43:df               A0[0][0]:uq

            // v58[v35 * 8 + v41] = v43 * float('0x3bf0000000000000')
            add<1>               V44:w                V42:w                V40:w               
            addr_add<1>          A1[0:1]:A            &V58+0               V44.(uw[1]):uw      
            mul<1>               A1[0][0:]:df         V43:df               0x3bf0000000000000:df

            // # BRKFOR
            add<1>               V41:d                V41:d                0x1:d               
            cmp.eq<1>            P1                   V41:d                0x8:d               
            jmp<1>(!P1)          BB_3_4
        
        // # BRKFOR
        add<1>               V35:d                V35:d                0x1:d               
        cmp.eq<1>            P2                   V35:d                0x8:d               
        jmp<1>(!P2)          BB_2_3

    // v45[:4] = tsc[:4]
    mov<4>               V45[0:]:d            tsc[0:]:G           
    mov<1>               V46:d                0x0:d               

BB_4_5:
    // for v46 in range(1, 8):
        // # skip 0
        cmp.eq<1>            P3                   V46:d                0x0:d               
        jmp<1>(P3)           BB_8_9

        // v47 = v46 * 8
        // v48 = v46 * 64
        shl<1>               V47:w                V46.(w[2])[0]:w      0x3:w               
        shl<1>               V48:w                V46.(w[2])[0]:w      0x6:w               
        mov<1>               V49:d                0x0:d               

BB_5_6:
        // for v49 in range(0, v46):
            // v50[:4] = tsc[:4]
            mov<4>               V50[0:]:d            tsc[0:]:G
            // v51 = v45[0] - v50[0]
            add<1>               V51.(d[1]):d         V45[0]:d             (-)V50[0]:d         
            cmp.lt<1>            P4                   V51[0]:b             0x0:b
            jmp<1>(P4)           BB_6_7              
            // if v51.tochar() >= 0:
                // v57 = v58[v46 * 8 + v49]
                mov<1>               V52:w                0x8:w               
                mad<1>               V53:w                V49.(w[2])[0]:w      V52:w                V48:w
                addr_add<1>          A2[0:1]:A            &V58+0               V53.(uw[1]):uw      
                mov<1>               V57:df               A2[0][0]:df
                // v56p = (v49 * 8) + v46
                mov<1>               V56:w                0x40:w              
                mad<1>               V56:w                V49.(w[2])[0]:w      V56:w                V47:w
                jmp<1>               BB_7_8              
BB_6_7:
            // else:
                // v57 = v58[v49 * 8 + v46]
                mov<1>               V54:w                0x40:w              
                mad<1>               V55:w                V49.(w[2])[0]:w      V54:w                V47:w
                addr_add<1>          A3[0:1]:A            &V58+0               V55.(uw[1]):uw      
                mov<1>               V57:df               A3[0][0]:df         
                // v56p = v46 * 8 + v49
                mov<1>               V56:w                0x8:w               
                mad<1>               V56:w                V49.(w[2])[0]:w      V56:w                V48:w               

BB_7_8:
            // v58[v56p] = v57
            addr_add<1>          A4[0:1]:A            &V58+0               V56.(uw[1]):uw      
            mov<1>               A4[0][0:]:df         V57:df

            // # BRKFOR
            add<1>               V49:d                V49:d                0x1:d               
            cmp.eq<1>            P5                   V49:d                V46:d               
            jmp<1>(!P5)          BB_5_6              

BB_8_9:
        // # BRKFOR
        add<1>               V46:d                V46:d                0x1:d               
        cmp.eq<1>            P6                   V46:d                0x8:d               
        jmp<1>(!P6)          BB_4_5

    // v66[:8] = [0]
    mov<8>               V66[0:]:df           0x0:df              
    mov<1>               V59:d                0x0:d               

BB_9_10:
    // for v59 in range(0, 8):
        // v60 = v59 * 64
        shl<1>               V60:w                V59.(w[2])[0]:w      0x6:w               
        mov<1>               V61:d                0x0:d               

BB_10_11:
        // for v61 in range(0, 8):
            cmp.eq<1>            P7                   V61:d                V59:d
            // i5 = v59 * 8 + v61
            mov<1>               V62:w                0x8:w               
            mad<1>               V63:w                V61.(w[2])[0]:w      V62:w                V60:w
            addr_add<1>          A5[0:1]:A            &V66+0               V63.(uw[1]):uw

            jmp<1>(P7)           BB_11_12
            // if v61 != v59:
                // v66[i5] = 0.0
                mov<1>               A5[0][0:]:df         0x0:df              
                jmp<1>               BB_12_13            

BB_11_12:
            // else:
                // v66[i5] = float('0x3ff0000000000000')
                mov<1>               A5[0][0:]:df         0x3ff0000000000000:df

BB_12_13:
            // # BRKFOR
            add<1>               V61:d                V61:d                0x1:d               
            cmp.eq<1>            P8                   V61:d                0x8:d               
            jmp<1>(!P8)          BB_10_11

        // # BRKFOR
        add<1>               V59:d                V59:d                0x1:d               
        cmp.eq<1>            P9                   V59:d                0x8:d               
        jmp<1>(!P9)          BB_9_10

    // v64 = 0
    mov<1>               V64:d                0x0:d

    // v287 = v58[:]
    mov<8>               V287[0:]:df          V58[0:]:df          
    mov<8>               V287[8:]:df          V58[8:]:df          
    mov<8>               V287[16:]:df         V58[16:]:df         
    mov<8>               V287[24:]:df         V58[24:]:df         
    mov<8>               V287[32:]:df         V58[32:]:df         
    mov<8>               V287[40:]:df         V58[40:]:df         
    mov<8>               V287[48:]:df         V58[48:]:df         
    mov<8>               V287[56:]:df         V58[56:]:df         

BB_13_14:
    // for v64 in range(7):
        // v67[v64] = func_v287_tri_argmax(v64)
        mov<1>               V285:d               V64:d               
        call<1>              func_v287_tri_argmax
        shl<1>               V65:w                V64.(w[2])[0]:w      0x2:w               
        addr_add<1>          A6[0:1]:A            &V67+0               V65.(uw[1]):uw      
        mov<1>               A6[0][0:]:d          V286:d

        // # BRKFOR
        add<1>               V64:d                V64:d                0x1:d               
        cmp.eq<1>            P10                  V64:d                0x7:d               
        jmp<1>(!P10)         BB_13_14

    mov<1>               V68:d                0x0:d               

BB_15_16:
    // for v68 in range(0x800):
        // v69, v70 = func2()
        call<1>              func2

        // a7v = v287[v70 * 8 + v70]
        mul<1>               V71:w                V70.(w[2])[0]:w      0x48:w              
        addr_add<1>          A7[0:1]:A            &V287+0              V71.(uw[1]):uw

        // a8v = v287[v70 * 8 + v69]
        shl<1>               V72:w                V70.(w[2])[0]:w      0x6:w
        mov<1>               V73:w                0x8:w
        mad<1>               V74:w                V69.(w[2])[0]:w      V73:w                V72:w               
        addr_add<1>          A8[0:1]:A            &V287+0              V74.(uw[1]):uw

        // v75 = a7v + a8v
        add<1>               V75:df               A7[0][0]:df          A8[0][0]:df

        cmp.eq<1>            P11                  V75:df               A7[0][0]:df         
        jmp<1>(!P11)         BB_17_18
        // if v75 == a7v: # i.e. a8v == 0 ????
            // a9v = v287[v69 * 9]
            mul<1>               V76:w                V69.(w[2])[0]:w      0x48:w              
            addr_add<1>          A9[0:1]:A            &V287+0              V76.(uw[1]):uw
            
            // v77 = a8v + a9v
            add<1>               V77:df               A8[0][0]:df          A9[0][0]:df

            cmp.eq<1>            P12                  V77:df               A9[0][0]:df         
            jmp<1>(!P12)         BB_17_18
            // if v77 == a9v: # i.e. a8v == 0 ????
                // v287[v70 * 8 + v69] = 0
                mov<1>               A8[0][0:]:df         0x0:df

                // v67[v70] = func_v287_tri_argmax(v70)
                mov<1>               V285:d               V70:d               
                call<1>              func_v287_tri_argmax
                shl<1>               V78:w                V70.(w[2])[0]:w      0x2:w               
                addr_add<1>          A10[0:1]:A           &V67+0               V78.(uw[1]):uw      
                mov<1>               A10[0][0:]:d         V286:d              

BB_17_18:
        // func3(v70, v69)
        mov<1>               V175:d               V70:d               
        mov<1>               V176:d               V69:d               
        call<1>              func3

        // func4(v70, v69)
        mov<1>               V188:d               V70:d               
        mov<1>               V189:d               V69:d               
        call<1>              func4

        // v66 = func5(v66, v70, v69)
        call<1>              func5

        // # BRKFOR
        add<1>               V68:d                V68:d                0x1:d               
        cmp.eq<1>            P13                  V68:d                0x800:d             
        jmp<1>(!P13)         BB_15_16

    // v80 = [0.0] * 8
    mov<1>               V79:df               0x0:df
    mov<8>               V80[0:]:df           V79:df

    mov<1>               V81:d                0x0:d

    // v84 = [0.0] * 8
    mov<8>               V84[0:]:df           V80[0:]:df          

BB_21_22:
    // for v81 in range(0, 8):
        // v84[v81] = v287[v81 * 9]
        shl<1>               V82:w                V81.(w[2])[0]:w      0x3:w               
        mul<1>               V83:w                V81.(w[2])[0]:w      0x48:w
        addr_add<1>          A11[0:1]:A           &V287+0              V83.(uw[1]):uw      
        addr_add<1>          A12[0:1]:A           &V84+0               V82.(uw[1]):uw      
        mov<1>               A12[0][0:]:df        A11[0][0]:df

        // # BRKFOR
        add<1>               V81:d                V81:d                0x1:d               
        cmp.eq<1>            P14                  V81:d                0x8:d               
        jmp<1>(!P14)         BB_21_22

    // v87 = [0.0] * 64
    mov<8>               V87[0:]:df           0x0:df              
    mov<8>               V87[8:]:df           0x0:df              
    mov<8>               V87[16:]:df          0x0:df              
    mov<8>               V87[24:]:df          0x0:df              
    mov<8>               V87[32:]:df          0x0:df              
    mov<8>               V87[40:]:df          0x0:df              
    mov<8>               V87[48:]:df          0x0:df              
    mov<8>               V87[56:]:df          0x0:df

    mov<1>               V85:d                0x0:d               
BB_22_23:
    // for v85 in range(8):
        // v87[v85] = v84[v85]
        shl<1>               V86:w                V85.(w[2])[0]:w      0x3:w               
        addr_add<1>          A13[0:1]:A           &V84+0               V86.(uw[1]):uw      
        addr_add<1>          A14[0:1]:A           &V87+0               V86.(uw[1]):uw      
        mov<1>               A14[0][0:]:df        A13[0][0]:df

        // # BRKFOR
        add<1>               V85:d                V85:d                0x1:d               
        cmp.eq<1>            P15                  V85:d                0x8:d               
        jmp<1>(!P15)         BB_22_23

    mov<1>               V88:d                0x0:d

    // v94 = [None] * 49
    // v93 = [None] * 49
    lifetime.start       V94                 
    lifetime.start       V93                 

BB_23_24:
    // for v88 in range(8):
        // v91 = 0
        mov<1>               V89:d                0x0:d               
        mov<1>               V91:d                0x0:d               

BB_24_25:
        // for v89 in range(8):
            // p16 = v89 != v88
            cmp.ne<1>            P16                  V89:d                V88:d
            // v90 = 0
            mov<1>               V90:d                0x0:d               

BB_25_26:
            // for v90 in range(8)
                // if v90 == v88 or v89 == v88:
                    // continue
                cmp.ne<1>            P17                  V90:d                V88:d               
                and<1>               P18                  P16                  P17                 
                jmp<1>(!P18)         BB_26_27

                // v94[v91] = v89
                shl<1>               V92:w                V91.(w[2])[0]:w      0x2:w               
                addr_add<1>          A15[0:1]:A           &V94+0               V92.(uw[1]):uw
                mov<1>               A15[0][0:]:d         V89:d

                // v93[v91] = v90
                addr_add<1>          A16[0:1]:A           &V93+0               V92.(uw[1]):uw
                mov<1>               A16[0][0:]:d         V90:d

                // v91 += 1
                add<1>               V91:d                V91:d                0x1:d               

BB_26_27:
                // # BRKFOR
                add<1>               V90:d                V90:d                0x1:d               
                cmp.eq<1>            P19                  V90:d                0x8:d               
                jmp<1>(!P19)         BB_25_26

            // # BRKFOR
            add<1>               V89:d                V89:d                0x1:d
            cmp.eq<1>            P20                  V89:d                0x8:d               
            jmp<1>(!P20)         BB_24_25

        // w93 = trunc_to_words(v93) # i.e. drop higher 16 bytes
        // w94 = trunc_to_words(v94) # i.e. drop higher 16 bytes

        // # v102 [0:32], v100 [32:48], v101 [48:49]
        // v105 = v58[w94 * 8 + w93]

        mov<16>              V95[0:]:w            V93.(w[98])[0::2]:w
        mov<1>               V96:w                0x8:w               
        mad<16>              V102[0:]:w           V94.(w[98])[0::2]:w  V96:w                V95[0:]:w
        mov<16>              V97[0:]:w            V93.(w[98])[32::2]:w
        mov<1>               V98:w                0x8:w               
        mad<16>              V102[16:]:w          V94.(w[98])[32::2]:w V98:w                V97[0:]:w

        mov<16>              V100[0:]:w           V93.(w[98])[64::2]:w
        mov<1>               V99:w                0x8:w               
        mad<16>              V100[0:]:w           V94.(w[98])[64::2]:w V99:w                V100[0:]:w

        mov<1>               V101:w               0x8:w               
        mad<1>               V101:w               V94.(w[98])[96]:w    V101:w               V93.(w[98])[96]:w

        shl<32>              V102[0:]:w           V102[0:]:w           0x3:w               
        shl<16>              V103[0:]:w           V100[0:]:w           0x3:w
        shl<1>               V104:w               V101:w               0x3:w

        addr_add<8>          A17[0:8]:A           &V58+0               V102.(uw[32])[0:]:uw
        mov<8>               V105[0:]:df          A17[0:,0]:df               
        addr_add<8>          A18[0:8]:A           &V58+0               V102.(uw[32])[8:]:uw
        mov<8>               V105[8:]:df          A18[0:,0]:df               
        addr_add<8>          A19[0:8]:A           &V58+0               V102.(uw[32])[16:]:uw
        mov<8>               V105[16:]:df         A19[0:,0]:df               
        addr_add<8>          A20[0:8]:A           &V58+0               V102.(uw[32])[24:]:uw
        mov<8>               V105[24:]:df         A20[0:,0]:df

        addr_add<16>         A21[0:16]:A          &V58+0               V103.(uw[16])[0:]:uw
        mov<8>               V105[32:]:df         A21[0:,0]:df               
        mov<8>               V105[40:]:df         A21[8:,0]:df

        addr_add<1>          A22[0:1]:A           &V58+0               V104.(uw[1]):uw     
        mov<1>               V105[48:]:df         A22[0:,0]:df

        // v287[:8] = 0
        mov<8>               V287[0:]:df          0x0:df

        mov<1>               V106:d               0x0:d               
BB_27_28:
        // for v106 in range(8):
            cmp.eq<1>            P21                  V106:d               0x7:d

            // v107 = v106 * 64
            // v108 = v106 * 7 * 8
            shl<1>               V107:w               V106.(w[2])[0]:w     0x6:w               
            mul<1>               V108:w               V106.(w[2])[0]:w     0x38:w

            mov<1>               V109:d               0x0:d               
BB_28_29:
            // for v109 in range(8):
                cmp.eq<1>            P22                  V109:d               0x7:d               
                or<1>                P23                  P21                  P22
                shl<1>               V110:w               V109.(w[2])[0]:w     0x3:w
                jmp<1>(P23)          BB_29_30
                // if v109 != 7 and v106 != 7:
                    // v287[v106 * 8 + v109] = v105[v106 * 7 + v109]
                    mov<1>               V111:w               0x8:w               
                    mad<1>               V112:w               V109.(w[2])[0]:w     V111:w               V108:w              
                    addr_add<1>          A23[0:1]:A           &V105+0              V112.(uw[1]):uw
                    add<1>               V113:w               V110:w               V107:w              
                    addr_add<1>          A24[0:1]:A           &V287+0              V113.(uw[1]):uw     
                    mov<1>               A24[0][0:]:df        A23[0][0]:df        
                    jmp<1>               BB_30_31            

BB_29_30:
                // else:
                    // v287[v106 * 8 + v109] = 0
                    add<1>               V114:w               V110:w               V107:w              
                    addr_add<1>          A25[0:1]:A           &V287+0              V114.(uw[1]):uw     
                    mov<1>               A25[0][0:]:df        0x0:df              

BB_30_31:
                // # BRKFOR
                add<1>               V109:d               V109:d               0x1:d               
                cmp.eq<1>            P24                  V109:d               0x8:d               
                jmp<1>(!P24)         BB_28_29

            // # BRKFOR
            add<1>               V106:d               V106:d               0x1:d               
            cmp.eq<1>            P25                  V106:d               0x8:d               
            jmp<1>(!P25)         BB_27_28

        // # XXX: Removed loop. WTF is this loop ????
        mov<1>               V115:d               0x0:d               
BB_31_32:
        add<1>               V115:d               V115:d               0x1:d               
        cmp.eq<1>            P26                  V115:d               0x8:d

        // v116 = 0
        mov<1>               V116:d               0x0:d               
        jmp<1>(!P26)         BB_31_32            

BB_32_33:
        // for v116 in range(0, 7):
            // v67[v116] = func_v287_tri_argmax(v116)
            mov<1>               V285:d               V116:d              
            call<1>              func_v287_tri_argmax
            shl<1>               V117:w               V116.(w[2])[0]:w     0x2:w               
            addr_add<1>          A26[0:1]:A           &V67+0               V117.(uw[1]):uw     
            mov<1>               A26[0][0:]:d         V286:d

            // # BRKFOR
            add<1>               V116:d               V116:d               0x1:d               
            cmp.eq<1>            P27                  V116:d               0x7:d               
            jmp<1>(!P27)         BB_32_33

        mov<1>               V118:d               0x0:d               
BB_33_34:
        // for v118 in range(0, 0x800):
            // v69, v70 = func2()
            call<1>              func2

            // a27v = v287[v70 * 8 + v70]
            mul<1>               V119:w               V70.(w[2])[0]:w      0x48:w              
            addr_add<1>          A27[0:1]:A           &V287+0              V119.(uw[1]):uw

            // i28 = v70 * 8 + v69
            shl<1>               V120:w               V70.(w[2])[0]:w      0x6:w               
            mov<1>               V121:w               0x8:w               
            mad<1>               V122:w               V69.(w[2])[0]:w      V121:w               V120:w
            addr_add<1>          A28[0:1]:A           &V287+0              V122.(uw[1]):uw

            // v123 = a27v + v287[i28]
            add<1>               V123:df              A27[0][0]:df         A28[0][0]:df
            
            cmp.eq<1>            P28                  V123:df              A27[0][0]:df        
            jmp<1>(!P28)         BB_34_35
            // if v123 == a27v: # i.e. v287[i28] == 0 ???
                // a29v = v287[v69 * 9]
                mul<1>               V124:w               V69.(w[2])[0]:w      0x48:w              
                addr_add<1>          A29[0:1]:A           &V287+0              V124.(uw[1]):uw

                // v125 = v287[i28] + a29v
                add<1>               V125:df              A28[0][0]:df         A29[0][0]:df

                cmp.eq<1>            P29                  V125:df              A29[0][0]:df        
                jmp<1>(!P29)         BB_34_35
                // if v125 == a29v: # i.e. v287[i28] == 0 ???
                    // v287[i28] = 0
                    mov<1>               A28[0][0:]:df        0x0:df

                    // v67[v70] = func_v287_tri_argmax(v70)
                    mov<1>               V285:d               V70:d               
                    call<1>              func_v287_tri_argmax
                    shl<1>               V126:w               V70.(w[2])[0]:w      0x2:w               
                    addr_add<1>          A30[0:1]:A           &V67+0               V126.(uw[1]):uw     
                    mov<1>               A30[0][0:]:d         V286:d              

BB_34_35:
            // func3(v70, v69)
            mov<1>               V175:d               V70:d               
            mov<1>               V176:d               V69:d               
            call<1>              func3

            // func4(v70, v69)
            mov<1>               V188:d               V70:d               
            mov<1>               V189:d               V69:d               
            call<1>              func4

            // # BRKFOR
            add<1>               V118:d               V118:d               0x1:d               
            cmp.eq<1>            P30                  V118:d               0x800:d             
            jmp<1>(!P30)         BB_33_34

        
        mov<1>               V127:d               0x0:d

        // v130 = v80[:8]
        mov<8>               V130[0:]:df          V80[0:]:df          

BB_35_36:
        // for v127 in range(8):
            // v130[v127] = v287[v127 * 9]
            shl<1>               V128:w               V127.(w[2])[0]:w     0x3:w               
            mul<1>               V129:w               V127.(w[2])[0]:w     0x48:w              
            addr_add<1>          A31[0:1]:A           &V287+0              V129.(uw[1]):uw     
            addr_add<1>          A32[0:1]:A           &V130+0              V128.(uw[1]):uw     
            mov<1>               A32[0][0:]:df        A31[0][0]:df

            // # BRKFOR
            add<1>               V127:d               V127:d               0x1:d               
            cmp.eq<1>            P31                  V127:d               0x8:d               
            jmp<1>(!P31)         BB_35_36

        // v131 = v88 * 7 + 8
        mul<1>               V131:d               V88:d                0x7:d               
        add<1>               V131:d               V131:d               0x8:d

        mov<1>               V132:d               0x0:d               
BB_36_37:
        // for v132 in range(7):
            // v87[v88 * 7 + v132 + 8] = v130[v132]
            shl<1>               V133:w               V132.(w[2])[0]:w     0x3:w               
            addr_add<1>          A33[0:1]:A           &V130+0              V133.(uw[1]):uw
            add<1>               V134.(d[1]):d        V131:d               V132:d              
            shl<1>               V135:w               V134[0]:w            0x3:w               
            addr_add<1>          A34[0:1]:A           &V87+0               V135.(uw[1]):uw     
            mov<1>               A34[0][0:]:df        A33[0][0]:df

            // # BRKFOR
            add<1>               V132:d               V132:d               0x1:d               
            cmp.eq<1>            P32                  V132:d               0x7:d               
            jmp<1>(!P32)         BB_36_37

        // # BRKFOR
        add<1>               V88:d                V88:d                0x1:d               
        cmp.eq<1>            P33                  V88:d                0x8:d               
        jmp<1>(!P33)         BB_23_24

    // v66 = v34 * abs(v66)
    mul<8>               V66[0:]:df           V34[0:]:df           (abs)V66[0:]:df     
    mul<8>               V66[8:]:df           V34[8:]:df           (abs)V66[8:]:df     
    mul<8>               V66[16:]:df          V34[16:]:df          (abs)V66[16:]:df    
    mul<8>               V66[24:]:df          V34[24:]:df          (abs)V66[24:]:df    
    mul<8>               V66[32:]:df          V34[32:]:df          (abs)V66[32:]:df    
    mul<8>               V66[40:]:df          V34[40:]:df          (abs)V66[40:]:df    
    mul<8>               V66[48:]:df          V34[48:]:df          (abs)V66[48:]:df    
    mul<8>               V66[56:]:df          V34[56:]:df          (abs)V66[56:]:df


    // v33 *= 1024
    shl<1>               V33:d                V33:d                0xa:d

    // v156[:256] = 0
    mov<16>              V156.(d[128])[0:]:d  0x0:d               
    mov<16>              V156.(d[128])[16:]:d 0x0:d               
    mov<16>              V156.(d[128])[32:]:d 0x0:d               
    mov<16>              V156.(d[128])[48:]:d 0x0:d

    // v156 = func_double_vec_to_byte_vec(v87)
    addr_add<1>          A39[0:1]:A           &V87+0               0x0:uw              
    call<1>              func_double_vec_to_byte_vec

    mov<1>               V136:d               0x0:d               
BB_38_39:
    // for v136 in range(32):
        shl<1>               V138.(d[1]):d        V136:d               0x4:d

        mov<1>               V137:d               0x400:d             
        mad<1>               V137:d               V32:uw               V137:d               V138.(d[1]):d

        // v139 = v156[v136 * 16:][:16]
        addr_add<1>          A35[0:1]:A           &V156+0              V138[0]:uw
        mov<16>              V139[0:]:ub          A35[0][0:]:ub

        // v140 = thread_y * 64 + v136
        shr<1>               V140:ud              V137.(ud[1]):ud      0x4:ud

        // out_t7[v140:v140+16] = v139
        oword_st             (1)                  T7                   V140(0,0)<0;1,0>     V139.0

        // # BRKFOR
        add<1>               V136:d               V136:d               0x1:d               
        cmp.eq<1>            P34                  V136:d               0x20:d              
        jmp<1>(!P34)         BB_38_39

    // v156 = func_double_vec_to_byte_vec(v66)
    addr_add<1>          A39[0:1]:A           &V66+0               0x0:uw              
    call<1>              func_double_vec_to_byte_vec

    // v33 += 0x200
    add<1>               V33:d                V33:d                0x200:d

    mov<1>               V141:d               0x0:d               
BB_39_40:
    // for v141 in range(32):
        shl<1>               V143.(d[1]):d        V141:d               0x4:d               
        add<1>               V142:d               V33:d                V143.(d[1]):d

        // v144 = v156[v141 * 16][:16]
        addr_add<1>          A36[0:1]:A           &V156+0              V143[0]:uw
        mov<16>              V144[0:]:ub          A36[0][0:]:ub

        // v145 = thread_y * 64 + 32 + v141
        shr<1>               V145:ud              V142.(ud[1]):ud      0x4:ud

        // out_t7[v145:v145+16] = v144
        oword_st             (1)                  T7                   V145(0,0)<0;1,0>     V144.0

        // # BRKFOR
        add<1>               V141:d               V141:d               0x1:d               
        cmp.eq<1>            P35                  V141:d               0x20:d              
        jmp<1>(!P35)         BB_39_40

    ret<1>              

.function "getDataMatrix"

func_getDataMatrixId:
// # _Z13getDataMatrixIdEv15cm_surfaceindexiu2CMmr8x8_T__BB_1_2_1
// def func_getDataMatrixId(v146):
    // v148 = inp_t8[v146 * 64:][:64]
    shl<1>               V146:d               V146:d               0x2:d               
    and<1>               V147:d               V146:d               0xffffffc:d         
    oword_ld             (4)                  T8                   V147.(ud[1])(0,0)<0;1,0> V148.0

    mov<1>               V149:d               0x0:d               
BB_40_41:
    // for v149 in range(8):
        shl<1>               V150:d               V149:d               0x3:d               
        shl<1>               V151:w               V149.(w[2])[0]:w     0x6:w

        mov<1>               V152:d               0x0:d               
BB_41_42:
        // for v152 in range(8):
            // v34[v149 * 8 + v152] = v148[v149 * 8 + v152]
            add<1>               V153.(d[1]):d        V152:d               V150:d              
            addr_add<1>          A37[0:1]:A           &V148+0              V153[0]:uw
            shl<1>               V154:w               V152.(w[2])[0]:w     0x3:w               
            add<1>               V155:w               V154:w               V151:w              
            addr_add<1>          A38[0:1]:A           &V34+0               V155.(uw[1]):uw     
            mov<1>               A38[0][0:]:df        A37[0][0]:ub

            // # BRKFOR
            add<1>               V152:d               V152:d               0x1:d               
            cmp.eq<1>            P36                  V152:d               0x8:d               
            jmp<1>(!P36)         BB_41_42

        // # BRKFOR
        add<1>               V149:d               V149:d               0x1:d               
        cmp.eq<1>            P37                  V149:d               0x8:d               
        jmp<1>(!P37)         BB_40_41

    // return v34
    ret<1>              

.function "func_double_vec_to_byte_vec"

func_double_vec_to_byte_vec:
// # _Z31convertDoubleVectorToByteVectorILi64EEvu2CMvrT__du2CMvrmlT_L_38_37
// def func_double_vec_to_byte_vec(a39):
    mov<1>               V157:d               0x0:d               
BB_42_43:
    // for v157 in range(64):
        // v158 = v157 // 8
        shl<1>               V158:w               V157.(w[2])[0]:w     0x3:w

        addr_add<1>          A40[0:1]:A           A39[0:1]:A           V158.(uw[1]):uw
        addr_add<1>          A41[0:1]:A           &V156+0              V158.(uw[1]):uw

        // v156[v158] = a39[v158].tobytes()
        mov<1>               A41[0][0:]:b         A40[0][0]:ub        
        shr<1>               V159.(uq[1]):uq      A40[0][0]:uq         0x8:uq              
        mov<1>               A41[0][1:]:b         V159[0]:ub          
        shr<1>               V160.(uq[1]):uq      A40[0][0]:uq         0x10:uq             
        mov<1>               A41[0][2:]:b         V160[0]:ub          
        shr<1>               V161.(uq[1]):uq      A40[0][0]:uq         0x18:uq             
        mov<1>               A41[0][3:]:b         V161[0]:ub          
        shr<1>               V162.(uq[1]):uq      A40[0][0]:uq         0x20:uq             
        mov<1>               A41[0][4:]:b         V162[0]:ub          
        shr<1>               V163.(uq[1]):uq      A40[0][0]:uq         0x28:uq             
        mov<1>               A41[0][5:]:b         V163[0]:ub          
        shr<1>               V164.(uq[1]):uq      A40[0][0]:uq         0x30:uq             
        mov<1>               A41[0][6:]:b         V164[0]:ub          
        shr<1>               V165.(uq[1]):uq      A40[0][0]:uq         0x38:uq             
        mov<1>               A41[0][7:]:b         V165[0]:ub

        // # BRKFOR
        add<1>               V157:d               V157:d               0x1:d               
        cmp.eq<1>            P38                  V157:d               0x40:d              
        jmp<1>(!P38)         BB_42_43

    // return v156
    ret<1>              

.function "func2"

func2:
// # _Z16JPYgRtzJnMjnpuDbIdEvu2CMmr8x8_T_RiS2__BB_16_17_16:
// def func2():
    // # global v67, v287
    // v69 = v67[0]
    mov<1>               V69:d                V67[0]:d

    // v167 = abs(v287[v67[0]])
    shl<1>               V166:w               V67.(w[16])[0]:w     0x3:w
    addr_add<1>          A42[0:1]:A           &V287+0              V166.(uw[1]):uw     
    mov<1>               V167:df              (abs)A42[0][0]:df
    // v168 = v167
    // v70 = 0
    mov<1>               V168:df              V167:df             
    mov<1>               V70:d                0x0:d               
    mov<1>               V169:d               0x1:d               

BB_43_44:
    // for v169 in range(1, 7):
        shl<1>               V170:w               V169.(w[2])[0]:w     0x2:w               
        addr_add<1>          A43[0:1]:A           &V67.(w[16])+0       V170.(uw[1]):uw

        // v174 = abs(v287[v169 * 8 + v67[v169]])
        shl<1>               V171:w               V169.(w[2])[0]:w     0x6:w               
        mov<1>               V172:w               0x8:w               
        mad<1>               V173:w               A43[0][0]:w          V172:w               V171:w
        addr_add<1>          A44[0:1]:A           &V287+0              V173.(uw[1]):uw     
        mov<1>               V174:df              (abs)A44[0][0]:df

        // if v174 > v168:
            // v69 = v67[v169]
            // v70 = v169
        cmp.gt<1>            P39                  V174:df              V168:df             
        sel<1>(P39)          V69:d                A43[0][0]:d          V69:d               
        sel<1>(P39)          V70:d                V169:d               V70:d

        // v168 = max(v174, v168)
        max<1>               V168:df              V174:df              V168:df

        // # BRKFOR
        add<1>               V169:d               V169:d               0x1:d               
        cmp.eq<1>            P40                  V169:d               0x7:d               
        jmp<1>(!P40)         BB_43_44            
    ret<1>
    // return v69, v70

.function "func3"

// # _Z16kpxrVWpHldSWgSHyIdEvu2CMmr8x8_T_ii_BB_18_19_18
// def func3(v175, v176):
func3:
    // a45v = v287[v176 * 9]
    mul<1>               V178:w               V176.(w[2])[0]:w     0x48:w              
    addr_add<1>          A45[0:1]:A           &V287+0              V178.(uw[1]):uw

    // v179 = v175 * 64
    shl<1>               V179:w               V175.(w[2])[0]:w     0x6:w
    
    // a46v = v287[v175 * 9]
    mul<1>               V180:w               V175.(w[2])[0]:w     0x48:w              
    addr_add<1>          A46[0:1]:A           &V287+0              V180.(uw[1]):uw

    // v181 = a45v - a46v
    add<1>               V181:df              A45[0][0]:df         (-)A46[0][0]:df

    // v177 = float('0x3ff0000000000000')
    mov<1>               V177:df              0x3ff0000000000000:df

    cmp.ne<1>            P41                  V181:df              0x0:df              
    jmp<1>(!P41)         BB_44_45
    // if v181 != 0:
        // a47v = v287[v175 * 8 + v176]
        mov<1>               V182:w               0x8:w               
        mad<1>               V183:w               V176.(w[2])[0]:w     V182:w               V179:w              
        addr_add<1>          A47[0:1]:A           &V287+0              V183.(uw[1]):uw

        // v177 = 0
        mov<1>               V177:df              0x0:df              
        cmp.ne<1>            P42                  A47[0][0]:df         0x0:df              
        jmp<1>(!P42)         BB_44_45
        // if a47v != 0:
            // v184 = a47v * float('0x4000000000000000')
            mul<1>               V184:df              A47[0][0]:df         0x4000000000000000:df
            // v181 = v181 / v184
            div<1>               V181:df              V181:df              V184:df
            // v185 = v181 * v181 + float('0x3ff0000000000000')
            mov<1>               V185:df              0x3ff0000000000000:df
            mad<1>               V185:df              V181:df              V181:df              V185:df
            // v185 = sqrtm(v185)
            sqrtm<1>             V185:df              V185:df
            // v186 = abs(v181)
            mov<1>               V186:df              (abs)V181:df
            // v177 = 1/(v185 + v186)
            add<1>               V177:df              V185:df              V186:df             
            inv<1>               V177:df              V177:df

            cmp.lt<1>            P43                  V181:df              0x0:df              
            jmp<1>(!P43)         BB_44_45
            // if v181 < 0:
                // v177 = -v177
                mov<1>               V177:df              (-)V177:df          

BB_44_45:
    // v187 = v177 * v177 + float('0x3ff0000000000000')
    mov<1>               V187:df              0x3ff0000000000000:df
    mad<1>               V187:df              V177:df              V177:df              V187:df
    // v187 = sqrtm(v187)
    sqrtm<1>             V187:df              V187:df
    // v190 = 1/v187
    inv<1>               V190:df              V187:df
    // v191 = v177 * v190
    mul<1>               V191:df              V177:df              V190:df             
    ret<1>
    // # export v177, v190, v191

.function "func4"

func4:
// # _Z16MlHoUTcdUynRDLWqIdEvu2CMmr8x8_T_ii_BB_19_20_19
// def func4(v188, v189):
    // # global v177, v190, v191
    // v192 = v188 * 8
    // v193 = v188 * 64
    // v194 = v189 * 8
    shl<1>               V192:w               V188.(w[2])[0]:w     0x3:w               
    shl<1>               V193:w               V188.(w[2])[0]:w     0x6:w               
    shl<1>               V194:w               V189.(w[2])[0]:w     0x3:w

    // i48 = v188 * 8 + v189
    mov<1>               V195:w               0x8:w               
    mad<1>               V196:w               V189.(w[2])[0]:w     V195:w               V193:w              
    addr_add<1>          A48[0:1]:A           &V287+0              V196.(uw[1]):uw

    // v197 = v287[i48] * v177
    mul<1>               V197:df              A48[0][0]:df         V177:df

    // i49 = v188 * 8 + v188
    mul<1>               V198:w               V188.(w[2])[0]:w     0x48:w              
    addr_add<1>          A49[0:1]:A           &V287+0              V198.(uw[1]):uw

    // v287[i49] -= v197
    add<1>               V199:w               V192:w               V193:w              
    addr_add<1>          A50[0:1]:A           &V287+0              V199.(uw[1]):uw
    add<1>               A50[0][0:]:df        A49[0][0]:df         (-)V197:df

    // v200 = v287[i48] * v177
    mul<1>               V200:df              A48[0][0]:df         V177:df

    // v201 = v189 * 64
    shl<1>               V201:w               V189.(w[2])[0]:w     0x6:w

    // i51 = v189 * 8 + v189
    mul<1>               V202:w               V189.(w[2])[0]:w     0x48:w              
    addr_add<1>          A51[0:1]:A           &V287+0              V202.(uw[1]):uw

    // v287[i51] += v200
    add<1>               V203:w               V194:w               V201:w              
    addr_add<1>          A52[0:1]:A           &V287+0              V203.(uw[1]):uw     
    add<1>               A52[0][0:]:df        V200:df              A51[0][0]:df

    // v287[i48] = 0
    mov<1>               A48[0][0:]:df        0x0:df

    
    cmp.gt<1>            P44                  V188:d               0x0:d               
    jmp<1>(!P44)         BB_49_50
    // if v188 > 0:
        mov<1>               V204:d               0x0:d               
BB_45_46:
        // for v204 in range(0, v188):
            // v205 = v204 * 8
            // v206 = v204 * 64
            shl<1>               V205:w               V204.(w[2])[0]:w     0x3:w               
            shl<1>               V206:w               V204.(w[2])[0]:w     0x6:w
            
            // i53 = v204 * 8 + v188
            mov<1>               V207:w               0x40:w              
            mad<1>               V208:w               V204.(w[2])[0]:w     V207:w               V192:w              
            addr_add<1>          A53[0:1]:A           &V287+0              V208.(uw[1]):uw

            // v287[v188 * 8 + v204] = v287[i53]
            add<1>               V209:w               V205:w               V193:w              
            addr_add<1>          A54[0:1]:A           &V287+0              V209.(uw[1]):uw     
            mov<1>               A54[0][0:]:df        A53[0][0]:df

            // v210 = v287[i53] * v190
            mul<1>               V210:df              A53[0][0]:df         V190:df

            // v213 = v287[v204 * 8 + v189] * v191
            mov<1>               V211:w               0x40:w              
            mad<1>               V212:w               V204.(w[2])[0]:w     V211:w               V194:w              
            addr_add<1>          A55[0:1]:A           &V287+0              V212.(uw[1]):uw
            mul<1>               V213:df              A55[0][0]:df         V191:df

            // v287[i53] = v210 - v213
            add<1>               A53[0][0:]:df        V210:df              (-)V213:df

            // a56v = v67[v204]
            shl<1>               V214:w               V204.(w[2])[0]:w     0x2:w               
            addr_add<1>          A56[0:1]:A           &V67+0               V214.(uw[1]):uw
            
            cmp.eq<1>            P45                  A56[0][0]:d          V188:d              
            jmp<1>(P45)          BB_46_47
            // if a56v != v188:
                // v215 = abs(v287[i53])
                mov<1>               V215:df              (abs)A53[0][0]:df

                // v218 = abs(v287[v204 * 8 + a56v])
                mov<1>               V216:w               0x8:w               
                mad<1>               V217:w               A56[0][0]:w          V216:w               V206:w              
                addr_add<1>          A57[0:1]:A           &V287+0              V217.(uw[1]):uw     
                mov<1>               V218:df              (abs)A57[0][0]:df

                cmp.gt<1>            P46                  V215:df              V218:df             
                jmp<1>(!P46)         BB_48_49
                // if v215 > v218:
                    // continue

                // v286 = v188
                mov<1>               V286:d               V188:d              
                jmp<1>               BB_47_48            
BB_46_47:
            // else:
                // v286 = func_v287_tri_argmax(v204)
                mov<1>               V285:d               V204:d              
                call<1>              func_v287_tri_argmax

BB_47_48:
            // v67[v204] = v286
            mov<1>               A56[0][0:]:d         V286:d              

BB_48_49:
            // # BRKFOR
            add<1>               V204:d               V204:d               0x1:d               
            cmp.eq<1>            P47                  V204:d               V188:d              
            jmp<1>(!P47)         BB_45_46            

BB_49_50:
    // v252 = v188 + 1
    add<1>               V252:d               V188:d               0x1:d               
    cmp.lt<1>            P48                  V252:d               V189:d              
    jmp<1>(!P48)         BB_51_52
    mov<1>               V219:d               V252:d              
BB_50_51:
    // for v219 in range(v252, v189):
        // i58 = v188 * 8 + v219
        mov<1>               V220:w               0x8:w               
        mad<1>               V221:w               V219.(w[2])[0]:w     V220:w               V193:w              
        addr_add<1>          A58[0:1]:A           &V287+0              V221.(uw[1]):uw

        // v287[v219 * 8 + v188] = v287[i58]
        shl<1>               V222:w               V219.(w[2])[0]:w     0x6:w               
        add<1>               V223:w               V192:w               V222:w              
        addr_add<1>          A59[0:1]:A           &V287+0              V223.(uw[1]):uw
        mov<1>               A59[0][0:]:df        A58[0][0]:df

        // v224 = v287[i58] * v190
        mul<1>               V224:df              A58[0][0]:df         V190:df

        // v227 = v287[v219 * 8 + v189] * v191
        mov<1>               V225:w               0x40:w              
        mad<1>               V226:w               V219.(w[2])[0]:w     V225:w               V194:w              
        addr_add<1>          A60[0:1]:A           &V287+0              V226.(uw[1]):uw
        mul<1>               V227:df              A60[0][0]:df         V191:df

        // v287[i58] = v224 - v227
        add<1>               A58[0][0:]:df        V224:df              (-)V227:df

        // # BRKFOR
        add<1>               V219:d               V219:d               0x1:d               
        cmp.eq<1>            P49                  V219:d               V189:d              
        jmp<1>(!P49)         BB_50_51            

BB_51_52:
    // v265 = v189 + 1
    add<1>               V265:d               V189:d               0x1:d               
    cmp.lt<1>            P50                  V189:d               0x7:d               
    jmp<1>(!P50)         BB_53_54            
    mov<1>               V228:d               V265:d
BB_52_53:
    // for v228 in range(v265, 8):
        // i61 = v188 * 8 + v228
        mov<1>               V229:w               0x8:w               
        mad<1>               V230:w               V228.(w[2])[0]:w     V229:w               V193:w              
        addr_add<1>          A61[0:1]:A           &V287+0              V230.(uw[1]):uw

        // v287[v228 * 8 + v188] = v287[i61]
        shl<1>               V231:w               V228.(w[2])[0]:w     0x6:w               
        add<1>               V232:w               V192:w               V231:w              
        addr_add<1>          A62[0:1]:A           &V287+0              V232.(uw[1]):uw     
        mov<1>               A62[0][0:]:df        A61[0][0]:df

        // v233 = v287[i61] * v190
        mul<1>               V233:df              A61[0][0]:df         V190:df

        // v236 = v287[v189 * 8 + v228] * v191
        mov<1>               V234:w               0x8:w               
        mad<1>               V235:w               V228.(w[2])[0]:w     V234:w               V201:w              
        addr_add<1>          A63[0:1]:A           &V287+0              V235.(uw[1]):uw
        mul<1>               V236:df              A63[0][0]:df         V191:df

        // v287[i61] = v233 - v236
        add<1>               A61[0][0:]:df        V233:df              (-)V236:df

        // # BRKFOR
        add<1>               V237:d               V228:d               0x1:d               
        cmp.lt<1>            P51                  V228:d               0x7:d               
        jmp<1>(!P51)         BB_53_54            
        mov<1>               V228:d               V237:d              
        jmp<1>               BB_52_53            

BB_53_54:
    // v67[v188] = func_v287_tri_argmax(v188)
    mov<1>               V285:d               V188:d              
    call<1>              func_v287_tri_argmax
    shl<1>               V238:w               V188.(w[2])[0]:w     0x2:w               
    addr_add<1>          A64[0:1]:A           &V67+0               V238.(uw[1]):uw     
    mov<1>               A64[0][0:]:d         V286:d

    // # p44 = V188 > 0
    jmp<1>(!P44)         BB_58_59            
    mov<1>               V239:d               0x0:d               
BB_54_55:
    // for v239 in range(v188):
        // i65 = v188 * 8 + v239
        mov<1>               V240:w               0x8:w               
        mad<1>               V241:w               V239.(w[2])[0]:w     V240:w               V193:w              
        addr_add<1>          A65[0:1]:A           &V287+0              V241.(uw[1]):uw

        // v242 = v287[i65] * v191
        mul<1>               V242:df              A65[0][0]:df         V191:df

        // v243 = v239 * 64
        shl<1>               V243:w               V239.(w[2])[0]:w     0x6:w

        // i66 = v239 * 8 + v189
        mov<1>               V244:w               0x40:w              
        mad<1>               V245:w               V239.(w[2])[0]:w     V244:w               V194:w              
        addr_add<1>          A66[0:1]:A           &V287+0              V245.(uw[1]):uw
        
        // v287[i66] = v287[i66] * v190 + v242
        mul<1>               V246:df              A66[0][0]:df         V190:df             
        add<1>               A66[0][0:]:df        V242:df              V246:df

        // a67v = v67[v239]
        shl<1>               V247:w               V239.(w[2])[0]:w     0x2:w               
        addr_add<1>          A67[0:1]:A           &V67+0               V247.(uw[1]):uw

        cmp.eq<1>            P52                  A67[0][0]:d          V189:d              
        jmp<1>(P52)          BB_55_56
        // if a67v != v189:
            // v248 = abs(v287[i66])
            mov<1>               V248:df              (abs)A66[0][0]:df

            // v251 = abs(v287[v239 * 8 + a67v])
            mov<1>               V249:w               0x8:w               
            mad<1>               V250:w               A67[0][0]:w          V249:w               V243:w              
            addr_add<1>          A68[0:1]:A           &V287+0              V250.(uw[1]):uw     
            mov<1>               V251:df              (abs)A68[0][0]:df
            
            cmp.gt<1>            P53                  V248:df              V251:df             
            jmp<1>(!P53)         BB_57_58
            // if v248 > v251:
                // continue

            // v286 = v189
            mov<1>               V286:d               V189:d              
            jmp<1>               BB_56_57            

BB_55_56:
        // else:
            // v286 = func_v287_tri_argmax(v239)
            mov<1>               V285:d               V239:d              
            call<1>              func_v287_tri_argmax

BB_56_57:
        // v67[v239] = v286
        mov<1>               A67[0][0:]:d         V286:d              

BB_57_58:
        // # BRKFOR
        add<1>               V239:d               V239:d               0x1:d               
        cmp.eq<1>            P54                  V239:d               V188:d              
        jmp<1>(!P54)         BB_54_55            

BB_58_59:
    jmp<1>(!P48)         BB_63_64            
BB_59_60:
    // for v252 in range(v252, v189):
        // v253 = v252 * 64
        shl<1>               V253:w               V252.(w[2])[0]:w     0x6:w

        // v256 = v287[v252 * 8 + v188] * v191
        mov<1>               V254:w               0x40:w              
        mad<1>               V255:w               V252.(w[2])[0]:w     V254:w               V192:w              
        addr_add<1>          A69[0:1]:A           &V287+0              V255.(uw[1]):uw
        mul<1>               V256:df              A69[0][0]:df         V191:df

        // i70 = v252 * 8 + v189
        mov<1>               V257:w               0x40:w              
        mad<1>               V258:w               V252.(w[2])[0]:w     V257:w               V194:w              
        addr_add<1>          A70[0:1]:A           &V287+0              V258.(uw[1]):uw

        // v287[i70] = v287[i70] * v190 + v256
        mul<1>               V259:df              A70[0][0]:df         V190:df             
        add<1>               A70[0][0:]:df        V256:df              V259:df

        // a71v = v67[v252]
        shl<1>               V260:w               V252.(w[2])[0]:w     0x2:w               
        addr_add<1>          A71[0:1]:A           &V67+0               V260.(uw[1]):uw

        cmp.eq<1>            P55                  A71[0][0]:d          V189:d              
        jmp<1>(P55)          BB_60_61
        // if a71v != v189:
            // v251 = abs(v287[i70])
            mov<1>               V261:df              (abs)A70[0][0]:df

            // v264 = abs(v287[v252 * 8 + a71v])
            mov<1>               V262:w               0x8:w               
            mad<1>               V263:w               A71[0][0]:w          V262:w               V253:w              
            addr_add<1>          A72[0:1]:A           &V287+0              V263.(uw[1]):uw
            mov<1>               V264:df              (abs)A72[0][0]:df

            cmp.gt<1>            P56                  V261:df              V264:df             
            jmp<1>(!P56)         BB_62_63
            // if v261 > v264:
                // continue

            // v286 = v189
            mov<1>               V286:d               V189:d              
            jmp<1>               BB_61_62            
BB_60_61:
        // else:
            // v286 = func_v287_tri_argmax(v252)
            mov<1>               V285:d               V252:d              
            call<1>              func_v287_tri_argmax

BB_61_62:
        // v67[v252] = v286
        mov<1>               A71[0][0:]:d         V286:d              

BB_62_63:
        // # BRKFOR
        add<1>               V252:d               V252:d               0x1:d               
        cmp.eq<1>            P57                  V252:d               V189:d              
        jmp<1>(!P57)         BB_59_60            

BB_63_64:
    jmp<1>(!P50)         BB_65_66            
BB_64_65:
    // for v265 in range(v265, 8):
        // v268 = v287[v265 * 8 + v188] * v191
        mov<1>               V266:w               0x40:w
        mad<1>               V267:w               V265.(w[2])[0]:w     V266:w               V192:w              
        addr_add<1>          A73[0:1]:A           &V287+0              V267.(uw[1]):uw
        mul<1>               V268:df              A73[0][0]:df         V191:df

        // v271 = v287[v189 * 8 + v265] * v190
        mov<1>               V269:w               0x8:w               
        mad<1>               V270:w               V265.(w[2])[0]:w     V269:w               V201:w              
        addr_add<1>          A74[0:1]:A           &V287+0              V270.(uw[1]):uw
        mul<1>               V271:df              A74[0][0]:df         V190:df

        // v287[v189 * 8 + v265] = v271 + v268
        add<1>               A74[0][0:]:df        V268:df              V271:df

        // # BRKFOR
        add<1>               V272:d               V265:d               0x1:d               
        cmp.lt<1>            P58                  V265:d               0x7:d               
        jmp<1>(!P58)         BB_65_66            
        mov<1>               V265:d               V272:d              
        jmp<1>               BB_64_65            

BB_65_66:
    // v67[v189] = func_v287_tri_argmax(v189)
    mov<1>               V285:d               V189:d              
    call<1>              func_v287_tri_argmax
    shl<1>               V273:w               V189.(w[2])[0]:w     0x2:w               
    addr_add<1>          A75[0:1]:A           &V67+0               V273.(uw[1]):uw     
    mov<1>               A75[0][0:]:d         V286:d
    
    ret<1>              

.function "func5"

// # _Z16cdnzEgsXDUQhMTJHIdEvu2CMmr8x8_T_ii_BB_20_21_20
// def func5(v66, v70, v69):
    // # global v66, v190, v191
func5:
    // v274 = v70 * 64
    // v275 = v69 * 64
    shl<1>               V274:w               V70.(w[2])[0]:w      0x6:w               
    shl<1>               V275:w               V69.(w[2])[0]:w      0x6:w

    mov<1>               V276:d               0x0:d               
BB_66_67:
    // for v276 in range(8):
        // i76 = v70 * 8 + v276
        mov<1>               V277:w               0x8:w               
        mad<1>               V278:w               V276.(w[2])[0]:w     V277:w               V274:w              
        addr_add<1>          A76[0:1]:A           &V66+0               V278.(uw[1]):uw

        // v283 = v66[i76]
        mov<1>               V283:df              A76[0][0]:df

        // v279 = v66[i76] * v190
        mul<1>               V279:df              A76[0][0]:df         V190:df

        // i77 = v69 * 8 + v276
        mov<1>               V280:w               0x8:w               
        mad<1>               V281:w               V276.(w[2])[0]:w     V280:w               V275:w              
        addr_add<1>          A77[0:1]:A           &V66+0               V281.(uw[1]):uw

        // v282 = v66[i77] * v191
        mul<1>               V282:df              A77[0][0]:df         V191:df

        // v66[i76] = v279 - v282
        add<1>               A76[0][0:]:df        V279:df              (-)V282:df

        // v283 = v283 * v191
        mul<1>               V283:df              V283:df              V191:df

        // v284 = v66[i77] * v190
        mul<1>               V284:df              A77[0][0]:df         V190:df

        // v66[i77] = v283 + v284
        add<1>               A77[0][0:]:df        V283:df              V284:df

        // # BRKFOR
        add<1>               V276:d               V276:d               0x1:d               
        cmp.eq<1>            P59                  V276:d               0x8:d               
        jmp<1>(!P59)         BB_66_67

    // return v66
    ret<1>              

.function "func_v287_tri_argmax"

// # _Z16aAqwvgDTmHcpllEMIdEiu2CMmr8x8_T_i_BB_14_15_14:
// def func_v287_tri_argmax(v285):
func_v287_tri_argmax:
    // v286 = v285 + 1
    add<1>               V286:d               V285:d               0x1:d               
    add<1>               V289:d               V285:d               0x2:d

    cmp.lt<1>            P60                  V285:d               0x6:d               
    jmp<1>(!P60)         BB_68_69
    // if v285 < 6:
        shl<1>               V288:w               V285.(w[2])[0]:w     0x6:w               

BB_67_68:
        // for v289 in range(v285 + 2, 8):
            // v292 = abs(v287[v285 * 8 + v289])
            mov<1>               V290:w               0x8:w               
            mad<1>               V291:w               V289.(w[2])[0]:w     V290:w               V288:w
            addr_add<1>          A78[0:1]:A           &V287+0              V291.(uw[1]):uw     
            mov<1>               V292:df              (abs)A78[0][0]:df

            // v295 = abs(v287[v285 * 8 + v286])
            mov<1>               V293:w               0x8:w               
            mad<1>               V294:w               V286.(w[2])[0]:w     V293:w               V288:w
            addr_add<1>          A79[0:1]:A           &V287+0              V294.(uw[1]):uw     
            mov<1>               V295:df              (abs)A79[0][0]:df

            // if v292 > v295:
                // v286 = v289
            cmp.gt<1>            P61                  V292:df              V295:df             
            sel<1>(P61)          V286:d               V289:d               V286:d

            // # BRKFOR
            add<1>               V296:d               V289:d               0x1:d               
            cmp.lt<1>            P62                  V289:d               0x7:d               
            jmp<1>(!P62)         BB_68_69
            mov<1>               V289:d               V296:d              
            jmp<1>               BB_67_68            

BB_68_69:
    ret<1>
    // return v286

