function 1
    portout[1]=1
    portout[9]=1
    do in 19000
        portout[9]=0
    end
end;

function 2
    portout[2]=1
    portout[10]=1
    do in 19000
        portout[10]=0
    end
end;

function 3
    portout[3]=1
    portout[11]=1
    do in 19000
        portout[11]=0
    end
end;

function 4
    portout[4]=1
    portout[12]=1
    do in 19000
        portout[12]=0
    end
end;

function 5
    portout[5]=1
    portout[13]=1
    do in 19000
        portout[13]=0
    end
end;

function 6
    portout[6]=1
    portout[14]=1
    do in 19000
        portout[14]=0
    end
end;

function 7
    portout[7]=1
    portout[15]=1
    do in 19000
        portout[15]=0
    end
end;

function 8
    trigger(1)
    do in 10
        trigger(2)
    end
    do in 20
        trigger(3)
    end
    do in 30
        trigger(4)
    end
    do in 20000
        trigger(5)
    end
    do in 20050
        trigger(6)
    end
    do in 20060
        trigger(7)
    end
end;

trigger(8)

;