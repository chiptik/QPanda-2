from numpy import pi
from pyqpanda import *
import time
PI = 3.1415926535898


def utilities_fun():

    machine = init_quantum_machine(QMachineType.CPU)

    prog = QProg()
    q = machine.qAlloc_many(6)
    c = machine.cAlloc_many(6)

    prog.insert(H(q[0]))\
        .insert(Y(q[5]))\
        .insert(S(q[2]))\
        .insert(CZ(q[0], q[1]))

    print(to_QRunes(prog, machine))
    print(to_QASM(prog, machine))
    print(to_Quil(prog, machine))
    print(count_gate(prog, machine))
    print(get_clock_cycle(machine, prog))
    print(get_bin_str(prog, machine))

    machine.finalize()


def cpu_qvm_fun():

    machine = CPUQVM()
    machine.initQVM()

    prog_trans, qv, cv = convert_qasm_to_qprog("D:\\123.txt", machine)
    # print(result1)
    # print(result2)

    print(convert_qprog_to_originir(prog_trans, machine))

    machine.finalize()


def singleAmp_fun():

    machine = SingleAmpQVM()

    machine.initQVM()

    q = machine.qAlloc_many(10)
    c = machine.cAlloc_many(10)

    prog = QProg()

    prog.insert(hadamard_circuit(q))\
        .insert(CZ(q[1], q[5]))\
        .insert(CZ(q[3], q[5]))\
        .insert(CZ(q[2], q[4]))\
        .insert(CZ(q[3], q[7]))\
        .insert(CZ(q[0], q[4]))\
        .insert(RY(q[7], PI / 2))\
        .insert(RX(q[8], PI / 2))\
        .insert(RX(q[9], PI / 2))\
        .insert(CR(q[0], q[1], PI))\
        .insert(CR(q[2], q[3], PI))\
        .insert(RY(q[4], PI / 2))\
        .insert(RZ(q[5], PI / 4))\
        .insert(RX(q[6], PI / 2))\
        .insert(RZ(q[7], PI / 4))\
        .insert(CR(q[8], q[9], PI))\
        .insert(CR(q[1], q[2], PI))\
        .insert(RY(q[3], PI / 2))\
        .insert(RX(q[4], PI / 2))\
        .insert(RX(q[5], PI / 2))\
        .insert(CR(q[9], q[1], PI))\
        .insert(RY(q[1], PI / 2))\
        .insert(RY(q[2], PI / 2))\
        .insert(RZ(q[3], PI / 4))\
        .insert(CR(q[7], q[8], PI))

    machine.run(prog)

    # result1 = machine.pmeasure("6")
    # result2 = machine.pmeasure_bin_index(prog, "0000000000")
    # result3 = machine.pmeasure_dec_index(prog, "1")
    # result = machine.pmeasure("6")
    # print(result3)

    qlist = [q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9]]
    result4 = machine.get_prob_dict(qlist, "3")


def partialAmp_fun():

    machine = PartialAmpQVM()

    machine.init_qvm()

    q = machine.qAlloc_many(10)
    c = machine.cAlloc_many(10)

    prog = QProg()

    prog.insert(hadamard_circuit(q))\
        .insert(CZ(q[1], q[5]))\
        .insert(CZ(q[3], q[7]))\
        .insert(CZ(q[0], q[4]))\
        .insert(RZ(q[7], PI / 4))\
        .insert(RX(q[5], PI / 4))\
        .insert(RX(q[4], PI / 4))\
        .insert(RY(q[3], PI / 4))\
        .insert(CZ(q[2], q[6]))\
        .insert(RZ(q[3], PI / 4))\
        .insert(RZ(q[8], PI / 4))\
        .insert(CZ(q[9], q[5]))\
        .insert(RY(q[2], PI / 4))\
        .insert(RZ(q[9], PI / 4))\
        .insert(CZ(q[2], q[3]))

    print(to_originir(prog, machine))

    machine.run(prog)

    result2 = machine.pmeasure_bin_index("0000000000")
    result3 = machine.pmeasure_dec_index("1")

    qlist = ["0", "1", "2"]
    result4 = machine.pmeasure_subset(qlist)

    print(result2, result3, result4)


def graph_match_fun():

    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(4)
    c = machine.cAlloc_many(4)

    #           ┌─┐┌────┐┌─┐
    # q_0:  |0>─┤H├┤CNOT├┤H├───────────────
    #           └─┘└──┬─┘└─┘
    # q_1:  |0>───────■─────■──────────────
    #           ┌─┐      ┌──┴─┐┌─┐
    # q_2:  |0>─┤H├──────┤CNOT├┤H├───■─────
    #           ├─┤      └────┘└─┘┌──┴─┐┌─┐
    # q_3:  |0>─┤H├───────────────┤CNOT├┤H├
    #           └─┘               └────┘└─┘

    #           ┌──┐
    # q_0:  |0>─┤CZ├────────
    #           └─┬┘
    # q_1:  |0>───■───■─────
    #               ┌─┴┐
    # q_2:  |0>─────┤CZ├──■─
    #               └──┘┌─┴┐
    # q_3:  |0>─────────┤CZ├
    #                   └──┘

    prog = QProg()
    prog.insert(H(q[0]))\
        .insert(H(q[2]))\
        .insert(H(q[3]))\
        .insert(CNOT(q[1], q[0]))\
        .insert(H(q[0]))\
        .insert(CNOT(q[1], q[2]))\
        .insert(H(q[2]))\
        .insert(CNOT(q[2], q[3]))\
        .insert(H(q[3]))

    query_cir = QCircuit()
    query_cir.insert(H(q[0]))\
             .insert(CNOT(q[1], q[0]))\
             .insert(H(q[0]))

    replace_cir = QCircuit()
    replace_cir.insert(CZ(q[0], q[1]))

    print("before replace")
    print_qprog(prog)

    update_prog = graph_query_replace(prog, query_cir, replace_cir, machine)

    print("after replace")
    # print(to_originir(update_prog,machine))
    print_qprog(update_prog)


def QCloud_fun():

    QCM = QCloud()
    # QCM.init_qvm("C40A08F3D461481D829559EE7CCAA359")
    QCM.init_qvm("EE3DE52BFF2245908EA9F47EFC8D50A3")

    # QCM.set_compute_api(
    #     "10.10.12.140:8060/api/taskApi/submitTask.json")
    # QCM.set_inqure_api(
    #     "10.10.12.140:8060/api/taskApi/getTaskDetail.json")

    QCM.set_compute_api(
        "https://qcloud.qubitonline.cn/api/taskApi/submitTask.json")
    QCM.set_inqure_api(
        "https://qcloud.qubitonline.cn/api/taskApi/getTaskDetail.json")

    qlist = QCM.qAlloc_many(6)
    clist = QCM.cAlloc_many(6)

    measure_prog = QProg()
    measure_prog.insert(hadamard_circuit(qlist))\
                .insert(CZ(qlist[1], qlist[5]))\
                .insert(Measure(qlist[0], clist[0]))\
                .insert(Measure(qlist[1], clist[1]))

    pmeasure_prog = QProg()
    pmeasure_prog.insert(hadamard_circuit(qlist))\
                 .insert(CZ(qlist[1], qlist[5]))\
                 .insert(RX(qlist[2], PI / 4))\
                 .insert(RX(qlist[1], PI / 4))\

    # result0 = QCM.full_amplitude_measure(measure_prog, 100)
    # print(result0)
    # print("full_amplitude_measure pass !")

    # result1 = QCM.full_amplitude_pmeasure(pmeasure_prog, [0, 1, 2])
    # print(result1)
    # print("full_amplitude_pmeasure pass !")

    # result2 = QCM.partial_amplitude_pmeasure(pmeasure_prog, ["0", "1", "2"])
    # print(result2)
    # print("partial_amplitude_pmeasure pass !")

    # result3 = QCM.single_amplitude_pmeasure(pmeasure_prog, "0")
    # print(result3)
    # print("single_amplitude_pmeasure pass !")

    # QCM.set_noise_model(NoiseModel.BIT_PHASE_FLIP_OPRATOR, [0.01], [0.02])
    # result4 = QCM.noise_measure(measure_prog, 100)
    # print(result4)
    # print("noise_measure pass !")

    result5 = QCM.real_chip_measure(measure_prog, 100)
    print(result5)
    print("real_chip_measure pass !")

    # result6 = QCM.get_state_tomography_density(measure_prog, 100)
    # print(result6)
    # print("get_state_tomography_density !")

    QCM.finalize()


def Cluster_Cloud():

    QCM = QCloud()
    QCM.initQVM()

    qlist = QCM.qAlloc_many(10)
    clist = QCM.cAlloc_many(10)

    prog = QProg()
    prog.insert(H(qlist[0]))\
        .insert(Measure(qlist[0], clist[0]))

    # task = QCM.full_amplitude_measure(prog, 100)
    # print(task)

    # time.sleep(3)
    result = QCM.get_cluster_result(
        ClusterMachineType.Full_AMPLITUDE, "2001061726139435101012920")
    # result = QCM.get_cluster_result(0, "2001061726139435101012920")

    QCM.finalize()


def noise_fun():
    qvm = NoiseQVM()
    qvm.set_configure(20, 20)

    # default argc
    qubits_num = 10
    shot = 100

    # 设置噪声模型参数
    noise_rate = 0.001
    qvm.set_noise_model(NoiseModel.DEPHASING_KRAUS_OPERATOR,
                        GateType.HADAMARD_GATE, [noise_rate])
    qvm.set_noise_model(NoiseModel.DEPHASING_KRAUS_OPERATOR,
                        GateType.CPHASE_GATE, [2 * noise_rate])

    qvm.init_qvm()

    q = qvm.qAlloc_many(qubits_num)
    c = qvm.cAlloc_many(qubits_num)

    prog = QProg()
    for i in range(0, qubits_num):
        target = q[qubits_num - 1 - i]
        prog.insert(H(target))
        for j in range(i + 1, qubits_num):
            control = q[qubits_num - 1 - j]
            prog.insert(CR(control, target, 2 * pi / (1 << (j - i + 1))))

    prog.insert(measure_all(q, c))

    start = time.time()
    result = qvm.run_with_configuration(prog, c, shot)
    end = time.time()
    print(qvm.get_allocate_cmem_num())
    print(qvm.get_allocate_qubit_num())
    print(qvm.getAllocateCMem())
    print(qvm.getAllocateQubitNum())
    print("noise :", "qubit =", qubits_num,
          " shots =", shot, " times =", end - start)
    # print(result)
    qvm.finalize()


def jkuqvm_fun():

    machine = JKUQVM()
    machine.set_configure(50, 50)
    machine.init_qvm()

    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = QProg()
    prog.insert(X1(q[0]))\
        .insert(Z1(q[0]))\
        .insert(Y1(q[0]))\
        .insert(Measure(q[0], c[0]))

    result = machine.run_with_configuration(prog, c, 100)
    print(result)

    machine.finalize()


if __name__ == "__main__":

    QCloud_fun()
    # cpu_qvm_fun()
    # singleAmp_fun()
    # partialAmp_fun()
    # Cluster_Cloud()
    # graph_match_fun()
    # noise_fun()
    # jkuqvm_fun()
