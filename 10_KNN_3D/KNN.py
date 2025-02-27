from os import system
import numpy as np
import scipy.optimize as op
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


####################################################################
def initTheta(X,degree):
    size=getThetaSizeFromDegree(X,degree)
    return np.zeros((size, 1))
####################################################################
def listToArray(xlist):
    return np.array(xlist)
def SaveData(data):
    np.savetxt("dataAfterKmean.csv", data, delimiter=",",fmt='%f')
    return

####################################################################
def addBiasVector(X):
    r=np.column_stack((np.ones((X.shape[0],1)),X))
    return r

def concatenateVectors(X,Y):
    r=np.column_stack((X,Y))

    return r
####################################################################
def clearScreen():
    system('cls')
    return

####################################################################
def loadData(fileName):
    data= np.loadtxt(fileName, delimiter=',')
    if (len(data.shape)==1):
        data.shape=(data.shape[0],1)
    return data



####################################################################
def plotPlane(theta,X,y):
    degree=getDegreeFromTheta(theta,X)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    #plt.subplot(122)    
    aX=X[:,0]
    aY=X[:,1]
    aZ=y
    ax.scatter(aX,aY,aZ,marker="o",color="r")
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    u = np.linspace(x_min, x_max,20) 
    v = np.linspace(y_min, y_max, 20) 
    z = np.zeros(( len(u), len(v) )) 
    U,V=np.meshgrid(u,v)
    for i in range(len(u)): 
        for j in range(len(v)): 
            uv= concatenateVectors(np.array([[u[i]]]),np.array([[v[j]]]))
            z[i,j] =np.sum( np.matmul(mapFeature(uv,degree),theta) )
    z = np.transpose(z) 
    ax.scatter(U,V,z,marker="+")
    plt.show()
####################################################################
def plotLine3d(theta1,theta,X,y):
    degree=getDegreeFromTheta(theta,X)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    #plt.subplot(122)    
    aX=X[:,0]
    aY=X[:,1]
    aZ=y
    ax.scatter(aX,aY,aZ,marker="o",color="r")
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    
    u = np.linspace(x_min, x_max,50) 
    u.shape=(len(u),1) 
    v=predict(theta1,u) 

    
    z = np.zeros( len(u)) 
    
    for i in range(len(u)): 
        uv= concatenateVectors(np.array([[u[i]]]),np.array([[v[i]]]))
        z[i] =np.sum( np.matmul(mapFeature(uv,degree),theta) )
    z = np.transpose(z) 
    ax.plot(u,v,z)
    plt.show()
####################################################################
def plotLine(theta,X,y):
    plt.subplot(122)
    plt.scatter(X,y) 

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    u = np.linspace(x_min, x_max, 100)
    u.shape=(len(u),1) 
    v=predict(theta,u) 
    plt.plot(u, v,color='r')
    plt.show()
    ####################################################################
def plotXY(X,y):
    # plt.subplot(122)
    plt.scatter(X,y,marker="+") 

    plt.show()
 ####################################################################

def getDegreeFromTheta(theta,X):
    sz=theta.shape[0]
    if (X.shape[1]==2):
        degree=(np.sqrt(sz*8+1)-3)/2
        degree=int(degree)
    else:
         degree=sz-1
    return degree

####################################################################
def getThetaSizeFromDegree(X,degree):
    sz=X.shape[1]
    if (sz==2):
        sz=(degree+1)*(degree+2)/2
        sz=int(sz)
    else:
         sz=degree+1
    return sz

####################################################################
def predict(theta,X):
    degree=getDegreeFromTheta(theta,X)
    X=mapFeature(X,degree)
    Py=np.matmul(X,theta)                      #Hypothesis 
    return Py

####################################################################
def accurracy(Y1,Y2):
    m=np.mean(Y1==Y2)   
    return m*100


####################################################################
def computeCost(theta,X,y):
    m = X.shape[0]
    h= X @ theta                      #Hypothesis
    h.shape=y.shape
    err=h-y
    errSqr=np.multiply(err,err)
    J=(1.0/(2.0*m))* np.sum(errSqr)
    return J

####################################################################
def mapFeature(X,degree):
    
    sz=getThetaSizeFromDegree(X,degree)
    out=np.ones((X.shape[0],sz))

    sz=X.shape[1]
    if (sz==2):
        X1=X[:, 0:1]
        X2=X[:, 1:2]
        col=1
        for i in range(1,degree+1):        
            for j in range(0,i+1):
                out[:,col:col+1]= np.multiply(np.power(X1,i-j),np.power(X2,j))    
                col+=1
        return out
    else:
        for i in range(1,degree+1):        
            out[:,i:i+1]= np.power(X,i)
    
    return out

####################################################################
def computeGradient(theta,X,y):
    m,n = X.shape
    theta.shape = (n,1) 
    h=np.matmul( X,theta)                      #Hypothesis
    h.shape=y.shape
    err=h-y
    d=np.dot(err.T,X)  
    g=  (1.0/m)*d
    return g.flatten()




####################################################################
def optimizedGradientDescent(X, y, theta,degree): 
    oldShape=theta.shape
    X=mapFeature(X,degree)
    myargs=(X, y[:,0])
    Result = op.minimize(fun = computeCost, x0 = theta.flatten(),  args =myargs, method = 'TNC',jac = computeGradient)
    theta = Result.x
    
   
    #theta = op.fmin(computeCost, x0=theta, args=myargs) 
    #theta,_,_,_,_,_,_= op.fmin_bfgs(computeCost, x0=theta, args=myargs, full_output=True) 
    theta.shape=oldShape

    return theta

####################################################################
def KMean_FindClosestCentroids(X,K, centroids):    
    K=centroids.shape[0]
    #Assign index to each training set
    idx=np.zeros((X.shape[0],1))
    for i in range(len(X[:,0:1])): 
        Prev_Distance=np.linalg.norm( X[i,:]-centroids[0,:])
        for j in range(1,K):
            Current_Distance=np.linalg.norm( X[i,:]-centroids[j,:])
            if(Current_Distance<=Prev_Distance):
                idx[i]=j
                Prev_Distance=Current_Distance
    return idx



####################################################################
def KMean_ComputeCentroids(X,K,idx):    
    centroids = np.zeros((K,X.shape[1]))
    for j in range(0,K):
        sumC=np.zeros((1,X.shape[1]))
        countC=0
        for i in range(len(X[:,0:1])): 
            if (idx[i]==j):
                sumC=sumC+X[i,:]
                countC=countC+1
        if (countC!=0):
            centroids[j,:]=(1/countC)*sumC

    return centroids


####################################################################
def KMean_Run(X,initial_centroids,max_iters):        
    centroids=initial_centroids
    K=centroids.shape[0]
    for i in range(max_iters):
        idx = KMean_FindClosestCentroids(X,K, centroids)
        centroids = KMean_ComputeCentroids(X, K,idx)
    return idx


   


####################################################################
def plotKmean(X,idx):
    # plt.subplot(122)
    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')
    ax.scatter(X[:,0:1],X[:,1:2],X[:,2:3],marker=".",facecolors='black', edgecolors='none') 
    ax = fig.add_subplot(122, projection='3d')
    ax.scatter(X[:,0:1],X[:,1:2],X[:,2:3],marker=".",facecolors='black', edgecolors='none') 
    ax.scatter(X[:,0:1][np.where(idx==0)],X[:,1:2][np.where(idx==0)],X[:,2:3][np.where(idx==0)],marker="o",facecolors='none', edgecolors='r')
    ax.scatter(X[:,0:1][np.where(idx==1)],X[:,1:2][np.where(idx==1)],X[:,2:3][np.where(idx==1)],marker="o",facecolors='none', edgecolors='b')
    ax.scatter(X[:,0:1][np.where(idx==2)],X[:,1:2][np.where(idx==2)],X[:,2:3][np.where(idx==2)],marker="o",facecolors='none', edgecolors='g')
    ax.scatter(X[:,0:1][np.where(idx==3)],X[:,1:2][np.where(idx==3)],X[:,2:3][np.where(idx==3)],marker="o",facecolors='none', edgecolors='m')

    plt.show()

####################################################################
def KNN_FindNearestClass(Xtrain,XClass,Xtest):
    m=Xtrain.shape[0]
    idx=np.zeros((Xtest.shape[0],1))
    for i in range(len(Xtest[:,0:1])): 
        Prev_Distance=np.linalg.norm( Xtest[i,:]-Xtrain[0,:])
        for j in range(1,m):
            Current_Distance=np.linalg.norm( Xtest[i,:]-Xtrain[j,:])
            if(Current_Distance<=Prev_Distance):
                idx[i]=XClass[j]
                Prev_Distance=Current_Distance
    return idx

####################################################################

def getcubeFaces(xpos,ypos,zpos,size):
    size=size/2
    points = np.array([[ -1*size +xpos, -1*size +ypos, -1*size +zpos],
                        [ 1*size +xpos, -1*size +ypos, -1*size +zpos ],
                        [ 1*size +xpos,  1*size +ypos, -1*size +zpos],
                        [-1*size +xpos,  1*size +ypos, -1*size +zpos],
                        [-1*size +xpos, -1*size +ypos,  1*size +zpos],
                        [ 1*size +xpos, -1*size +ypos,  1*size +zpos ],
                        [ 1*size +xpos,  1*size +ypos,  1*size +zpos],
                        [-1*size +xpos,  1*size +ypos,  1*size +zpos]])
    edges = [
            [points[0], points[1], points[2], points[3]],  #back 0-right -1- up -2 - left 3 -down -0
            [points[4], points[5], points[6], points[7]],  #front 4-right -5- up -6 - left 7 -down -4
            [points[0], points[4], points[7], points[3]], #left
            [points[1], points[5], points[6], points[2]], #right
            [points[3], points[7], points[6], points[2]],  #top
            [points[0], points[4], points[5], points[1]]   #bottom
            ]



    faces = Poly3DCollection(edges, linewidths=0, edgecolors='k')
    return faces
####################################################################

def plotKNN(X,idx):

    fig = plt.figure()
    
    
    
    ax = fig.add_subplot(111, projection='3d')
    

    
    


    x_min, x_max = X[:, 0].min() , X[:, 0].max() 
    y_min, y_max = X[:, 1].min() , X[:, 1].max() 
    z_min, z_max = X[:, 2].min() , X[:, 2].max() 
    u = np.linspace(x_min, x_max,10) 
    v = np.linspace(y_min, y_max,10) 
    w = np.linspace(z_min, z_max,10) 
    m=(len(u)*len(v)*len(w))
    u,v,w=np.meshgrid(u,v,w)
    u=u.reshape((m,1))
    v=v.reshape((m,1))
    w=w.reshape((m,1))
    NewX=concatenateVectors(concatenateVectors(u,v),w)
     
    NewIdx=KNN_FindNearestClass(X,idx,NewX)  

    

        
    ax.scatter(NewX[:,0:1][np.where(NewIdx==0)],NewX[:,1:2][np.where(NewIdx==0)],NewX[:,2:3][np.where(NewIdx==0)],marker="o",facecolors='r', edgecolors='r',s=100)
    ax.scatter(NewX[:,0:1][np.where(NewIdx==1)],NewX[:,1:2][np.where(NewIdx==1)],NewX[:,2:3][np.where(NewIdx==1)],marker="o",facecolors='b', edgecolors='b',s=100)
    ax.scatter(NewX[:,0:1][np.where(NewIdx==2)],NewX[:,1:2][np.where(NewIdx==2)],NewX[:,2:3][np.where(NewIdx==2)],marker="o",facecolors='g', edgecolors='g',s=100)



    #ORGINAL
    ax.scatter(X[:,0:1],X[:,1:2],X[:,2:3],marker=".",facecolors='black', edgecolors='none') 
    ax.scatter(X[:,0:1][np.where(idx==0)],X[:,1:2][np.where(idx==0)],X[:,2:3][np.where(idx==0)],marker="o",facecolors='none', edgecolors='r')
    ax.scatter(X[:,0:1][np.where(idx==1)],X[:,1:2][np.where(idx==1)],X[:,2:3][np.where(idx==1)],marker="o",facecolors='none', edgecolors='b')
    ax.scatter(X[:,0:1][np.where(idx==2)],X[:,1:2][np.where(idx==2)],X[:,2:3][np.where(idx==2)],marker="o",facecolors='none', edgecolors='g')
   
     
    plt.show()


####################################################################

def plotKNN2(X,idx):

    fig = plt.figure()
    
    
    
    ax = fig.add_subplot(111, projection='3d')
    

    
    


    x_min, x_max = X[:, 0].min() , X[:, 0].max() 
    y_min, y_max = X[:, 1].min() , X[:, 1].max() 
    z_min, z_max = X[:, 2].min() , X[:, 2].max() 
    u = np.linspace(x_min, x_max,10) 
    v = np.linspace(y_min, y_max,10) 
    w = np.linspace(z_min, z_max,10) 
    m=(len(u)*len(v)*len(w))
    u,v,w=np.meshgrid(u,v,w)
    u=u.reshape((m,1))
    v=v.reshape((m,1))
    w=w.reshape((m,1))
    NewX=concatenateVectors(concatenateVectors(u,v),w)
     
    NewIdx=KNN_FindNearestClass(X,idx,NewX)  

    

    #ORGINAL
    ax.scatter3D(X[:,0:1],X[:,1:2],X[:,2:3],marker="o",facecolors='black', edgecolors='black') 
  
    for i in range(m):
        faces = getcubeFaces(NewX[i,0],NewX[i,1],NewX[i,2],1)
        if (NewIdx[i]==0):
            faces.set_facecolor((0.5,0,0,0.05))
        if (NewIdx[i]==1):
            faces.set_facecolor((0,0,0.5,0.05))
        if (NewIdx[i]==2):
            faces.set_facecolor((0,0.5,0,0.05))
        ax.add_collection3d(faces)
   # faces = getcubeFaces(xpos,ypos,zpos,size)
   # faces.set_facecolor((0,0,1,0.5))
   # ax.add_collection3d(faces)


    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()