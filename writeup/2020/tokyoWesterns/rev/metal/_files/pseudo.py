    v32 = thread_y
    v33 = thread_y

    v34[:8] = 0

    v146 = thread_y

    v34 = func_getDataMatrixId(thread_y)

    v58 = [None] * 64
    for v35 in range(0, 8):
        v38 = thread_y * 64 + v35 * 8

        v39 = inp_t6[v38:v38+8]

        v40 = v35 * 8 * 8
        for v41 in range(0, 8):
            v43 = v39[v41]

            v58[v35 * 8 + v41] = v43 * _float('0x3bf0000000000000')

        

    v45[:4] = tsc[:4]
    for v46 in range(1, 8):
        # skip 0

        v47 = v46 * 8
        v48 = v46 * 64
        for v49 in range(0, v46):
            v50[:4] = tsc[:4]
            v51 = v45[0] - v50[0]
            if v51.tochar() >= 0:
                v57 = v58[v46 * 8 + v49]
                v56p = (v49 * 8) + v46
            else:
                v57 = v58[v49 * 8 + v46]
                v56p = v46 * 8 + v49
            v58[v56p] = v57


    v66[:8] = [0]
    for v59 in range(0, 8):
        v60 = v59 * 64
        for v61 in range(0, 8):
            i5 = v59 * 8 + v61
            if v61 != v59:
                v66[i5] = 0.0
            else:
                v66[i5] = _float('0x3ff0000000000000')


    v64 = 0

    v287 = v58[:]
    for v64 in range(7):
        v67[v64] = func_v287_tri_argmax(v64)

    for v68 in range(0x800):
        v69, v70 = func2()

        a7v = v287[v70 * 8 + v70]

        a8v = v287[v70 * 8 + v69]

        v75 = a7v + a8v
        if v75 == a7v: # i.e. a8v == 0 ????
            a9v = v287[v69 * 9]
            
            v77 = a8v + a9v
            if v77 == a9v: # i.e. a8v == 0 ????
                v287[v70 * 8 + v69] = 0

                v67[v70] = func_v287_tri_argmax(v70)
        func3(v70, v69)

        func4(v70, v69)

        v66 = func5(v66, v70, v69)


    v80 = [0.0] * 8

    v84 = [0.0] * 8
    for v81 in range(0, 8):
        v84[v81] = v287[v81 * 9]


    v87 = [0.0] * 64
    for v85 in range(8):
        v87[v85] = v84[v85]


    v94 = [None] * 49
    v93 = [None] * 49
    for v88 in range(8):
        v91 = 0
        for v89 in range(8):
            p16 = v89 != v88
            v90 = 0
            for v90 in range(8)
                if v90 == v88 or v89 == v88:
                    continue

                v94[v91] = v89

                v93[v91] = v90

                v91 += 1


        w93 = trunc_to_words(v93) # i.e. drop higher 16 bytes
        w94 = trunc_to_words(v94) # i.e. drop higher 16 bytes

        # v102 [0:32], v100 [32:48], v101 [48:49]
        v105 = v58[w94 * 8 + w93]


        v287[:8] = 0
        for v106 in range(8):

            v107 = v106 * 64
            v108 = v106 * 7 * 8
            for v109 in range(8):
                if v109 != 7 and v106 != 7:
                    v287[v106 * 8 + v109] = v105[v106 * 7 + v109]
                else:
                    v287[v106 * 8 + v109] = 0


        # XXX: Removed loop. WTF is this loop ????

        v116 = 0
        for v116 in range(0, 7):
            v67[v116] = func_v287_tri_argmax(v116)

        for v118 in range(0, 0x800):
            v69, v70 = func2()

            a27v = v287[v70 * 8 + v70]

            i28 = v70 * 8 + v69

            v123 = a27v + v287[i28]
            if v123 == a27v: # i.e. v287[i28] == 0 ???
                a29v = v287[v69 * 9]

                v125 = v287[i28] + a29v
                if v125 == a29v: # i.e. v287[i28] == 0 ???
                    v287[i28] = 0

                    v67[v70] = func_v287_tri_argmax(v70)
            func3(v70, v69)

            func4(v70, v69)


        v130 = v80[:8]
        for v127 in range(8):
            v130[v127] = v287[v127 * 9]


        v131 = v88 * 7 + 8
        for v132 in range(7):
            v87[v88 * 7 + v132 + 8] = v130[v132]



    v66 = v34 * abs(v66)


    v33 *= 1024

    v156[:256] = 0

    v156 = func_double_vec_to_byte_vec(v87)
    for v136 in range(32):
        v139 = v156[v136 * 16:][:16]
        v140 = thread_y * 64 + v136
        out_t7[v140:v140+16] = v139


    v156 = func_double_vec_to_byte_vec(v66)
    v33 += 0x200
    for v141 in range(32):
        v144 = v156[v141 * 16][:16]
        v145 = thread_y * 64 + 32 + v141
        out_t7[v145:v145+16] = v144


# _Z13getDataMatrixIdEv15cm_surfaceindexiu2CMmr8x8_T__BB_1_2_1
def func_getDataMatrixId(v146):
    v148 = inp_t8[v146 * 64:][:64]
    for v149 in range(8):
        for v152 in range(8):
            v34[v149 * 8 + v152] = v148[v149 * 8 + v152]



    return v34
# _Z31convertDoubleVectorToByteVectorILi64EEvu2CMvrT__du2CMvrmlT_L_38_37
def func_double_vec_to_byte_vec(a39):
    for v157 in range(64):
        v158 = v157 // 8

        v156[v158] = a39[v158].tobytes()


    return v156
# _Z16JPYgRtzJnMjnpuDbIdEvu2CMmr8x8_T_RiS2__BB_16_17_16:
def func2():
    # global v67, v287
    v69 = v67[0]

    v167 = abs(v287[v67[0]])
    v168 = v167
    v70 = 0
    for v169 in range(1, 7):

        v174 = abs(v287[v169 * 8 + v67[v169]])

        if v174 > v168:
            v69 = v67[v169]
            v70 = v169

        v168 = max(v174, v168)

    return v69, v70

# _Z16kpxrVWpHldSWgSHyIdEvu2CMmr8x8_T_ii_BB_18_19_18
def func3(v175, v176):
    a45v = v287[v176 * 9]

    v179 = v175 * 64
    
    a46v = v287[v175 * 9]

    v181 = a45v - a46v

    v177 = _float('0x3ff0000000000000')
    if v181 != 0:
        a47v = v287[v175 * 8 + v176]

        v177 = 0
        if a47v != 0:
            v184 = a47v * _float('0x4000000000000000')
            v181 = v181 / v184
            v185 = v181 * v181 + _float('0x3ff0000000000000')
            v185 = sqrtm(v185)
            v186 = abs(v181)
            v177 = 1/(v185 + v186)
            if v181 < 0:
                v177 = -v177
    v187 = v177 * v177 + _float('0x3ff0000000000000')
    v187 = sqrtm(v187)
    v190 = 1/v187
    v191 = v177 * v190
    # export v177, v190, v191
# _Z16MlHoUTcdUynRDLWqIdEvu2CMmr8x8_T_ii_BB_19_20_19
def func4(v188, v189):
    # global v177, v190, v191
    v192 = v188 * 8
    v193 = v188 * 64
    v194 = v189 * 8

    i48 = v188 * 8 + v189

    v197 = v287[i48] * v177

    i49 = v188 * 8 + v188

    v287[i49] -= v197

    v200 = v287[i48] * v177

    v201 = v189 * 64

    i51 = v189 * 8 + v189

    v287[i51] += v200

    v287[i48] = 0
    if v188 > 0:
        for v204 in range(0, v188):
            v205 = v204 * 8
            v206 = v204 * 64
            
            i53 = v204 * 8 + v188

            v287[v188 * 8 + v204] = v287[i53]

            v210 = v287[i53] * v190

            v213 = v287[v204 * 8 + v189] * v191

            v287[i53] = v210 - v213

            a56v = v67[v204]
            if a56v != v188:
                v215 = abs(v287[i53])

                v218 = abs(v287[v204 * 8 + a56v])
                if v215 > v218:
                    continue

                v286 = v188
            else:
                v286 = func_v287_tri_argmax(v204)
            v67[v204] = v286
    v252 = v188 + 1
    for v219 in range(v252, v189):
        i58 = v188 * 8 + v219

        v287[v219 * 8 + v188] = v287[i58]

        v224 = v287[i58] * v190

        v227 = v287[v219 * 8 + v189] * v191

        v287[i58] = v224 - v227

    v265 = v189 + 1
    for v228 in range(v265, 8):
        i61 = v188 * 8 + v228

        v287[v228 * 8 + v188] = v287[i61]

        v233 = v287[i61] * v190

        v236 = v287[v189 * 8 + v228] * v191

        v287[i61] = v233 - v236

    v67[v188] = func_v287_tri_argmax(v188)

    # p44 = V188 > 0
    for v239 in range(v188):
        i65 = v188 * 8 + v239

        v242 = v287[i65] * v191

        v243 = v239 * 64

        i66 = v239 * 8 + v189
        
        v287[i66] = v287[i66] * v190 + v242

        a67v = v67[v239]
        if a67v != v189:
            v248 = abs(v287[i66])

            v251 = abs(v287[v239 * 8 + a67v])
            if v248 > v251:
                continue

            v286 = v189
        else:
            v286 = func_v287_tri_argmax(v239)
        v67[v239] = v286
    for v252 in range(v252, v189):
        v253 = v252 * 64

        v256 = v287[v252 * 8 + v188] * v191

        i70 = v252 * 8 + v189

        v287[i70] = v287[i70] * v190 + v256

        a71v = v67[v252]
        if a71v != v189:
            v251 = abs(v287[i70])

            v264 = abs(v287[v252 * 8 + a71v])
            if v261 > v264:
                continue

            v286 = v189
        else:
            v286 = func_v287_tri_argmax(v252)
        v67[v252] = v286
    for v265 in range(v265, 8):
        v268 = v287[v265 * 8 + v188] * v191

        v271 = v287[v189 * 8 + v265] * v190

        v287[v189 * 8 + v265] = v271 + v268

    v67[v189] = func_v287_tri_argmax(v189)

# _Z16cdnzEgsXDUQhMTJHIdEvu2CMmr8x8_T_ii_BB_20_21_20
def func5(v66, v70, v69):
    # global v66, v190, v191
    v274 = v70 * 64
    v275 = v69 * 64
    for v276 in range(8):
        i76 = v70 * 8 + v276

        v283 = v66[i76]

        v279 = v66[i76] * v190

        i77 = v69 * 8 + v276

        v282 = v66[i77] * v191

        v66[i76] = v279 - v282

        v283 = v283 * v191

        v284 = v66[i77] * v190

        v66[i77] = v283 + v284


    return v66

# _Z16aAqwvgDTmHcpllEMIdEiu2CMmr8x8_T_i_BB_14_15_14:
def func_v287_tri_argmax(v285):
    v286 = v285 + 1
    if v285 < 6:
        for v289 in range(v285 + 2, 8):
            v292 = abs(v287[v285 * 8 + v289])

            v295 = abs(v287[v285 * 8 + v286])

            if v292 > v295:
                v286 = v289

    return v286

