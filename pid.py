def PIDcontrol(ballPosX, ballPosY, prevBallPosX, prevBallPosY, refX, refY):     # PID controller
    global totalErrorX, totalErrorY
    global alpha, beta, prevAlpha, prevBeta
    global startBalanceBall, arduinoIsConnected
    global Ts, delivery_time, N
    global prevDerivX, prevDerivY, prevIntegX, prevIntegY
    global prevErrorX, prevErrorY

    Ts = time.time() - delivery_time    #sampling time
    delivery_time = time.time()
    print(Ts)

    errorX = refX - ballPosX
    errorY = refY - ballPosY


    Kp = sliderCoefP.get()
    Ki = sliderCoefI.get()
    Kd = sliderCoefD.get()



    try:
        derivX = (prevBallPosX - ballPosX) / Ts
    except ZeroDivisionError:
        derivX = 0

    try:
        derivY = (prevBallPosY - ballPosY) / Ts
    except ZeroDivisionError:
        derivY = 0

    Cix = Ki * totalErrorX #prevIntegX + errorX*Ki*Ts                    #Ki * totalErrorX
    Ciy = Ki * totalErrorY #prevIntegY + errorY*Ki*Ts                    #Ki * totalErrorX




    Cdx =  Ts/(1+N*Ts)*(N*Kd*derivX + prevDerivX/Ts) #(Kd*N*(errorX-prevErrorX)+prevDerivX)/(1+N*Ts)# #Kd * ((errorX - prevErrorX)/Ts)
    Cdy =  Ts/(1+N*Ts)*(N*Kd*derivY + prevDerivY/Ts) #(Kd*N*(errorY-prevErrorY)+prevDerivY)/(1+N*Ts) # #Kd * ((errorY - prevErrorY)/Ts)

    Ix = Kp * errorX + Cix + Cdx
    Iy = Kp * errorY + Ciy + Cdy

    #Ix = Kp * (refX - ballPosX)
    #Iy = Kp * (refX - ballPosY)

    Ix = round(Ix, 1)
    Iy = round(Iy, 1)



    if Ix > max_alpha:
        Ix = max_alpha
    elif Ix < - max_alpha:
        Ix = - max_alpha
    if Iy > max_alpha:
        Iy = max_alpha
    elif Iy < - max_alpha:
        Iy = - max_alpha

    print(totalErrorX)

    if arduinoIsConnected == True and startBalanceBall == True:
        ser.write((str(dataDict[Ix]) + "," + str(dataDict[-Iy]) + "\n").encode())

    if startBalanceBall == True:
        prevDerivX = Cdx
        prevDerivY = Cdy
        prevIntegX = Cix
        prevIntegY = Ciy
        prevErrorX = errorX
        prevErrorY = errorY

prevX, prevY = 0, 0
prevRefX, prevRefY = 0, 0
start_time = 0
