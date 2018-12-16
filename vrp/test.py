file = open('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_polylines.txt', "r")

data = file.readlines()

# print("[")
# for line in data:
#     curr_line = line.strip("\n")
#     for char in curr_line:
#         if char in " []()":
#             curr_line.replace(char, '')
#     all_points = curr_line.split(",")
#     print(all_points[0:10])
#     pairs = "["
#     for i in range(0, 2, 2):
#         px = all_points[i].strip("[").strip("(").strip(")").strip("]")
#         if px[0] == " ":
#             px = px[1:]
#         if px[0] == "(":
#             px = px[1:]
#         py = all_points[i + 1].strip("[").strip("(").strip(")").strip("]")
#         pairs = pairs + "{lat:" + str(px) + ",lng:" + str(py) + "},"
#     px = all_points[i]
#     py = all_points[i + 1]
#     pairs = pairs + "{lat:" + str(px) + ",lng:" + str(py) + "}],"
#     print(pairs)
# print("]")

with open('input.txt', "r") as inp_file:
    with open('output.txt', "w") as out_file:
        data = inp_file.readlines()
        print(data)
        #for line in data:
        #    out_file.write(line.replace("\\", "\\\\"))

        polyline = "cuptHcm`YwCa@aCcAsByEaJcMwBiCiAu@_GoCcJcCiCsBuIwIO}@Do@a@iFWaDm@sDmAoDaFaLq@uB_AkIk@{D}@gCeMyQg@wAWsCAuASh@o[ft@eHzOyIrSo@n@o@T_@BeA_@aCiAkBwAeAeAc@MkCeDuRqVoKcKcF}DaF}CcI{DyJ{DiWuJ}XsKwLuFkMiHsTqNaPgKyMiIgLwFyMgFoK{C{GyAgKaByMmAkK[yF?eI@cH[eGw@oCm@oDoAiEiCiD{CeCiAsAIwAJ_AXqC`BqGdFsMfKiN|KeFzFiCdE{A~CoDnKgHxX_DjIyBjEoCfEaCvCgPdQkKxKcEfDyBtAeEjBcFpAmDj@eE\mDCiM}Aku@mLcI}@{CG}BFkCZ_Dx@wD~AmEzCsChCqG~GkIrIcErDmHbFoHjDwFzBgWlJ}K`DqFfAuMzAqRtAsNz@mFHkCG{Ce@_AUg@c@MIuA{@uCkD}GaLm@q@}BwAaBOm@Fm@PwA~@y@jAi@rAg@|B[hDOpGW|FWbD@p@uAfLuAvLgGvk@kA`NeC`d@oIp_BwCjl@]lLKhPTdSd@zLjBrYnLleB|@pURdOAbRQfMg@jNaAdQ_HrbAyJjwAgCxYeE|YuBhMs^`{BoFdZuOpq@u[jtAu^||AmYzmAuHt\oD~T_BxNmBnTyFnp@yCfXiBzKwCjNuC~KoHhTgHtO}Tvb@wC`HwCfImDdLiC`KaC`L{D`W}AzNoAnRq@|UG~U^`Sf@lLxAxRxGzl@dBfTdAbVPhPM`T{@lUoArPkC~X{LlqAuApMkDhUyBfKuDhNoUlv@kUru@wlAv~Dc{@fsCc\pfAkQ|h@qKnYwPlb@kWvo@oS|g@cLvYkKbZaO|e@gM~e@sQpu@aLdf@oD~Q}Fx[{Gr_@aF~Z_ObeAqDjTsEbVmT~hAcDlPc@|Bk@tAqA|FuAzCeA|AwBpBkFlDq@PyACm@GkBeA{CgBcE}BqZgQaHuFoCmCsCaCsE}C{Ai@eC_@oEg@eEyAcLqH{BqAaEyA{Cc@[Aq@AWWsADmANsCt@wBz@}DrBaMrGiCpAo@ZWLAKUeBUy@k@aAkAq@eDy@sBw@cFwEqEgEgCsCwHyLcBkCkEeFk@a@s@Mg@Fe@VaFhGgBzBgEtE}BvBgD~DwAxAqEzBmBn@oCv@qHvBc@AI_Ac@qA[Ws@@SJk@x@HvCObAy@t@oAp@qBz@wClAmA\kC|@wCjAeAx@q@~Aw@bAiK|Do@Lw@_@s@c@o@FyD~A}I`Dm@VQ`@DnDNfGIpF@nA"
        out_file.write(polyline)
