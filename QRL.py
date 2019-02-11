import openpyxl
wb = openpyxl.load_workbook("C:\\Users\\HP\\QRL\\Simulations_1.xlsx")
sheet = wb.create_sheet()
sheet.title = "Experment Set 11"

for nexp in range(0,1):
    from qiskit import IBMQ
    #IBMQ.enable_account('fa2b11e549562b53aa0e8fffda60344cbcd76f1f3f4b511d65eba76f0b36bcb3df52b4e392fae5c62f8e579cc24a6714e8cb002e4821b4d009edadca7ca8bd31', 'https://quantumexperience.ng.bluemix.net/api')
    #IBMQ.load_accounts()
    IBMQ.backends()
    backend = IBMQ.get_backend('ibmq_16_melbourne')
    shots = 1
    max_credits = 3
    
    import numpy as np
    #import matplotlib.pyplot as plt
    #matplotlib inline
    from math import pi
    
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
    from qiskit import available_backends, execute, register, get_backend
    from qiskit.tools.visualization import circuit_drawer
    from qiskit.tools.qi.qi import state_fidelity
    from qiskit import Aer
    
    #import xlwt
    #from xlwt import Workbook
    #wb = Workbook()
    #exp = wb.add_sheet('Experiment')
    #exp.write(0, 0+4*nexp, 'Iteration')
    #exp.write(0, 1+4*nexp, 'Delta')
    #exp.write(0, 2+4*nexp, 'Measurement')
    #exp.write(0, 3+4*nexp, 'Fidelity')
    sheet.cell(row=1, column=1+4*nexp).value = "Iteration"
    sheet.cell(row=1, column=2+4*nexp).value = "Delta"
    sheet.cell(row=1, column=3+4*nexp).value = "Measurement"
    sheet.cell(row=1, column=4+4*nexp).value = "Fidelity"
    
    import random 
    delta = pi
    eta = 0.75
    import array
    x = random.uniform(0, pi)
    #x = 0.8538402007092603
    y = random.uniform(0, 2*pi)
    #y = 0.9187448984647799
    z = random.uniform(0, 2*pi)
    #z = 0.0
    
    import math
    environment = [math.cos(x/2), complex(math.cos(y), math.sin(y))*math.sin(x/2)]
    count = 1
    
    q = QuantumRegister(3, 'q')
    c = ClassicalRegister(1)
    qc = QuantumCircuit(q,c)
    
    qc.u3(x,y,z,q[2])
    qc.cx(q[2],q[1])
    qc.measure(q[1],c[0])
    
    print(delta)
    job = execute(qc, backend=backend, shots=shots, max_credits=max_credits)
    result = job.result()
    result = result.get_counts(qc)
    m = str(result)
    print(m[4])
    #exp.write(1, 0+4*nexp, count)
    #exp.write(1, 1+4*nexp, delta)
    #exp.write(1, 2+4*nexp, m[4])
    sheet.cell(row=2, column=1+4*nexp).value = count
    sheet.cell(row=2, column=2+4*nexp).value = delta
    sheet.cell(row=2, column=3+4*nexp).value = m[4]
    
    if(m[4]=='1'):
        a = array.array('d',[random.uniform(-delta, delta)])
        b = array.array('d',[random.uniform(-delta, delta)])
        delta = delta/eta
    else:
        a = array.array('d',[0])
        b = array.array('d',[0])
        delta = delta*eta
        
    while count < 50:
        qc.reset(q[0])
        qc.reset(q[1])
        qc.reset(q[2])
        
        qc.u3(x,y,z,q[2])
        for j in range(0,len(a)):
            qc.rx(a[len(a)-1-j],q[0])
            qc.rz(b[len(a)-1-j],q[0])
            qc.rz(-b[j],q[2])
            qc.rx(-a[j],q[2])
        qc.cx(q[2],q[1])
        qc.measure(q[1],c[0])
        
        q1 = QuantumRegister(1, 'q1')
        qc1 = QuantumCircuit(q1)
        for j in range(0,len(a)):
            qc1.rx(a[len(a)-1-j],q1[0])
            qc1.rz(b[len(a)-1-j],q1[0])
    
        backend = Aer.get_backend('statevector_simulator')
        job = execute(qc1, backend)
        qc_state = job.result().get_statevector(qc1)
        qc_state
    
        f = state_fidelity(environment,qc_state)
        print(f)
        #exp.write(count, 3+4*nexp, f)
        sheet.cell(row=count+1, column=4+4*nexp).value = f
        
        print(delta)
        backend = IBMQ.get_backend('ibmq_16_melbourne')
        job = execute(qc, backend=backend, shots=shots, max_credits=max_credits)
        result = job.result()
        result = result.get_counts(qc)
        m = str(result)
        print(m[4])
        #exp.write(count+1, 0+4*nexp, count+1)
        #exp.write(count+1, 1+4*nexp, delta)
        #exp.write(count+1, 2+4*nexp, m[4])
        sheet.cell(row=count+2, column=1+4*nexp).value = count+1
        sheet.cell(row=count+2, column=2+4*nexp).value = delta
        sheet.cell(row=count+2, column=3+4*nexp).value = m[4]
        
        if(m[4]=='1'):
            a.append(random.uniform(-delta/2, delta/2))
            b.append(random.uniform(-delta/2, delta/2))
            delta = delta/eta
        else:
            a.append(0.0)
            b.append(0.0)
            delta = delta*eta
        
        wb.save("C:\\Users\\HP\\QRL\\Simulations_1.xlsx")
        count = count + 1
        
    q1 = QuantumRegister(1, 'q1')
    qc1 = QuantumCircuit(q1)
    for j in range(0,len(a)):
        qc1.rx(a[len(a)-1-j],q1[0])
        qc1.rz(b[len(a)-1-j],q1[0])
    
    backend = Aer.get_backend('statevector_simulator')
    job = execute(qc1, backend)
    qc_state = job.result().get_statevector(qc1)
    qc_state
    
    f = state_fidelity(environment,qc_state)
    print(f)
    #exp.write(count, 3+4*nexp, f)
    sheet.cell(row=count+1, column=4+4*nexp).value = f
    
    #exp.write(43, 0+4*nexp, 'x')
    #exp.write(43, 1+4*nexp, x)
    #exp.write(44, 0+4*nexp, 'y')
    #exp.write(44, 1+4*nexp, y)
    sheet.cell(row=53, column=1+4*nexp).value = "Delta"
    sheet.cell(row=53, column=2+4*nexp).value = pi
    sheet.cell(row=54, column=1+4*nexp).value = "Eta"
    sheet.cell(row=54, column=2+4*nexp).value = eta
    sheet.cell(row=55, column=1+4*nexp).value = "Theta"
    sheet.cell(row=55, column=2+4*nexp).value = x
    sheet.cell(row=56, column=1+4*nexp).value = "Phi"
    sheet.cell(row=56, column=2+4*nexp).value = y
    
    wb.save("C:\\Users\\HP\\QRL\\Simulations_1.xlsx")
    
#QASM_source = qc.qasm()
#print(QASM_source)
#circuit_drawer(qc)
