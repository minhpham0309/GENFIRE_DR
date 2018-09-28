"""
* genfire.reconstruct *

This module contains the core of GENFIRE's functions for computing reconstructions


Author: Alan (AJ) Pryor, Jr.
Jianwei (John) Miao Coherent Imaging Group
University of California, Los Angeles
Copyright 2015-2016. All rights reserved.
"""


from __future__ import division
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import os
import scipy.io
import time
import genfire
from multiprocessing import Pool
from genfire.utility import *

PI = np.pi
if __name__ != "__main__":
    def reconstruct(numIterations, initialObject, support, measuredK, constraintIndicators, constraintEnforcementDelayIndicators, R_freeInd_complex, R_freeVals_complex, displayFigure, use_positivity=True, use_support=True, method=1, verbose=True):
        """
         * reconstruct *

         Primary GENFIRE reconstruction function

        :param numIterations: Integer number of iterations to run
        :param initialObject: Initial guess of 3D object
        :param support: Binary matrix representing where the object is allowed to exist
        :param measuredK: Assembled 3D Fourier grid
        :param constraintIndicators: Flag value for each datapoint used to control during which iterations a given Fourier component is enforced
        :param constraintEnforcementDelayIndicators: List of cutoff values that will be divided evenly among the iterations. All Fourier grid points with constraintIndicators greater than the current cutoff are enforced
        :param R_freeInd_complex: 3 x 1 x num_shells tuple of (x,y,z) coordinate lists for withheld values for Rfree calculation
        :param R_freeVals_complex: Complex valued component at the indices given by R_freeInd_complex
        :param displayFigure: Boolean flag to display figures during the reconstruction
        :return: outputs dictionary containing the reconstruction and error metrics

         Author: Alan (AJ) Pryor, Jr.
         Jianwei (John) Miao Coherent Imaging Group
         University of California, Los Angeles
         Copyright 2015-2016. All rights reserved.
        """
        print(' ')
        import time
        t0 = time.time()
        if verbose:
            print("Reconstruction starting")
        bestErr = 1e30 #initialize error

        #initialize arrays for error metrics
        Rfree_complex = np.ones(numIterations)*-1 #
        errK = np.zeros(numIterations)

        #prefetch indices for monitoring error
        errInd = measuredK != 0

        #get dimensions of object
        dims = np.shape(support)
        if R_freeInd_complex:
            Rfree_complex_bybin = np.zeros((np.shape(R_freeInd_complex)[2], numIterations),dtype=float)
            Rfree_complex_total = np.zeros(numIterations,dtype=float)

        if displayFigure.DisplayFigureON: #setup some indices for plotting.
            n_half_x = int(dims[0]/2) #this assumes even-sized arrays
            n_half_y = int(dims[1]/2)
            n_half_z = int(dims[2]/2)

            half_window_x = displayFigure.reconstructionDisplayWindowSize[0]//2
            half_window_y = displayFigure.reconstructionDisplayWindowSize[1]//2
            half_window_z = displayFigure.reconstructionDisplayWindowSize[2]//2

        #setup output dict
        if R_freeInd_complex:
            outputs = {'reconstruction':initialObject,'errK':errK,'R_free_bybin':Rfree_complex_bybin, "R_free_total":Rfree_complex_total}
        else:
            outputs = {'reconstruction':initialObject,'errK':errK}

        #determine how to divide up the constraint enforcement cutoffs among the iterations by determining
        #which iterations will require a recalculation of the indices to enforce
        iterationNumsToChangeCutoff = np.round(np.linspace(1, numIterations, num=np.size(constraintEnforcementDelayIndicators)))
        iterationNumsToChangeCutoff, uniqueIndices = np.unique(iterationNumsToChangeCutoff, return_index=True)
        iterationNumsToChangeCutoff = np.append(iterationNumsToChangeCutoff,1e30) #add an arbitrarily high number to the end that is an iteration number that won't be reached
        constraintEnforcementDelayIndicators = constraintEnforcementDelayIndicators[uniqueIndices]
        currentCutoffNum = 0
		
		# ALGORITHMS: ER or DR
        if method==1:
          print('Starting ALTERNATING PROJECTION ALGORITHM')
		  # ALTERNATING PROJECTION (ERROR REDUCTION) ALGORITHM
          for iterationNum in range(1, numIterations+1): #iterations are counted started from 1
            #dt = 0.1 + 0.3*(1-np.sqrt((numIterations-iterationNum)/numIterations)) 

            if iterationNum == iterationNumsToChangeCutoff[currentCutoffNum]: #update current Fourier constraint if appropriate
                relevantCutoff = constraintEnforcementDelayIndicators[currentCutoffNum]
                constraintInd_complex = (constraintIndicators > relevantCutoff) * measuredK != 0
                #constraintInd_complex = measuredK !=0;

                bestErr = 1e30 #reset error
                currentCutoffNum+=1#update constraint set number

            #take FFT of current reconstruction
            k = fftn(initialObject)

            #compute error
            errK[iterationNum-1] = np.sum(abs(np.abs(k[errInd])-np.abs(measuredK[errInd])))/np.sum(abs(measuredK[errInd]))#monitor error
            if verbose:
                print("Iteration number: {0}/{1}           error = {2:0.5f}".format(iterationNum, numIterations, errK[iterationNum-1]))

            #update best object if a better one has been found
            if errK[iterationNum-1] < bestErr:
                bestErr = errK[iterationNum-1]
                outputs['reconstruction'] = initialObject

            #calculate Rfree for each spatial frequency shell if necessary
            if R_freeInd_complex:
                total_Rfree_error      = 0
                total_Rfree_error_norm = 0
                for shellNum in range(0, np.shape(R_freeInd_complex)[2]):

                    tmpIndX = R_freeInd_complex[0][0][shellNum]
                    tmpIndY = R_freeInd_complex[1][0][shellNum]
                    tmpIndZ = R_freeInd_complex[2][0][shellNum]

                    tmpVals = np.abs(R_freeVals_complex[shellNum])
                    # Rfree_numerator                         = np.sum(abs(k[tmpIndX, tmpIndY, tmpIndZ] - tmpVals))
                    Rfree_numerator                         = np.sum(abs(np.abs(k[tmpIndX, tmpIndY, tmpIndZ]) - tmpVals))
                    Rfree_denominator                       = np.sum(abs(tmpVals))
                    total_Rfree_error                      += Rfree_numerator
                    total_Rfree_error_norm                 += Rfree_denominator
                    Rfree_complex_bybin[shellNum, iterationNum-1] = Rfree_numerator / Rfree_denominator
                Rfree_complex_total[iterationNum-1] = total_Rfree_error / total_Rfree_error_norm
            #replace Fourier components with ones from measured data from the current set of constraints
            k[constraintInd_complex] = measuredK[constraintInd_complex]
            #k[constraintInd_complex] = dt*k[constraintInd_complex] + (1-dt)*measuredK[constraintInd_complex]
            initialObject = np.real(ifftn(k))
			
			#HIO ALGORITHM
            # if use_positivity:
                # initialObject[initialObject<0] = 0 #enforce positivity
            # if use_support:
                # initialObject = initialObject * support #enforce support

            #Object_temp = Object_old - 0.9*initialObject;
            #index_neg = (np.imag(initialObject)!=0) | (initialObject<0) | (initialObject!=0) & (support==0);
            #initialObject[index_neg] = np.copy(Object_temp[index_neg]);

            index_neg = (initialObject<0) | (support==0);
            initialObject[index_neg] = 0			

            #update display
            if displayFigure.DisplayFigureON:
                if iterationNum % displayFigure.displayFrequency == 0:
                    if verbose:
                        print("n_half_x = ", n_half_x)
                        print("half_window_y = ", half_window_y)
                    plt.figure(1000)
                    plt.subplot(233)
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central YZ slice")

                    plt.subplot(232)
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central XZ slice")

                    plt.subplot(231)
                    plt.title("central XY slice")
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z]))

                    plt.subplot(236)
                    plt.title("YZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=0)))

                    plt.subplot(235)
                    plt.title("XZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=1)))

                    plt.subplot(234)
                    plt.title("XY projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=2)))
                    plt.get_current_fig_manager().window.setGeometry(25,25,400, 400)
                    plt.draw()

                    plt.figure(2)
                    plt.get_current_fig_manager().window.setGeometry(25,450,400, 400)
                    plt.plot(range(0,numIterations),errK)
                    plt.title("K-space Error vs Iteration Number")
                    plt.xlabel("Spatial Frequency (% of Nyquist)")
                    plt.ylabel('Reciprocal Space Error')
                    plt.draw()

                    if R_freeInd_complex:
                        plt.figure(3)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,25,400, 400)
                        plt.plot(range(0,numIterations),Rfree_complex_total)
                        plt.title("Mean R-free Value vs Iteration Number")
                        plt.xlabel("Iteration Num")
                        plt.ylabel('Mean R-free')
                        plt.draw()

                        plt.figure(4)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,450,400, 400)
                        X = np.linspace(0,1,np.shape(Rfree_complex_bybin)[0])
                        plt.plot(X, Rfree_complex_bybin[:,iterationNum-1])
                        plt.title("Current Rfree Value vs Spatial Frequency")
                        plt.xlabel("Spatial Frequency (% of Nyquist)")
                        plt.ylabel('Rfree')
                        plt.draw()

                    if iterationNum<numIterations:
                        ptime=1
                    else:
                        ptime=100
                    plt.pause(ptime) #forces display to update
					
        else: # DR ALGORITHM
		  # ALGORITHM: u = u + P_O(2P_K - I)u - P_K*u
          print('Starting DOUGLAS RACHFORD ALGORITHM')		  
          k = fftn(initialObject)
          u = initialObject
          for iterationNum in range(1, numIterations+1): #iterations are counted started from 1
            dt = 0.1 #+ 0.3*(1-np.sqrt((numIterations-iterationNum)/numIterations)) 

            if iterationNum == iterationNumsToChangeCutoff[currentCutoffNum]: #update current Fourier constraint if appropriate
                relevantCutoff = constraintEnforcementDelayIndicators[currentCutoffNum]
                constraintInd_complex = (constraintIndicators > relevantCutoff) * measuredK != 0
                #constraintInd_complex = measuredK !=0;

                bestErr = 1e30 #reset error
                currentCutoffNum+=1#update constraint set number

            #take FFT of current reconstruction
            k = fftn(initialObject)

            #compute error
            errK[iterationNum-1] = np.sum(abs(np.abs(k[errInd])-np.abs(measuredK[errInd])))/np.sum(abs(measuredK[errInd]))#monitor error
            if verbose:
                print("Iteration number: {0}/{1}           error = {2:0.5f}".format(iterationNum, numIterations, errK[iterationNum-1]))

            #update best object if a better one has been found
            if errK[iterationNum-1] < bestErr:
                bestErr = errK[iterationNum-1]
                outputs['reconstruction'] = initialObject

            #calculate Rfree for each spatial frequency shell if necessary
            if R_freeInd_complex:
                total_Rfree_error      = 0
                total_Rfree_error_norm = 0
                for shellNum in range(0, np.shape(R_freeInd_complex)[2]):

                    tmpIndX = R_freeInd_complex[0][0][shellNum]
                    tmpIndY = R_freeInd_complex[1][0][shellNum]
                    tmpIndZ = R_freeInd_complex[2][0][shellNum]

                    tmpVals = np.abs(R_freeVals_complex[shellNum])
                    # Rfree_numerator                         = np.sum(abs(k[tmpIndX, tmpIndY, tmpIndZ] - tmpVals))
                    Rfree_numerator                         = np.sum(abs(np.abs(k[tmpIndX, tmpIndY, tmpIndZ]) - tmpVals))
                    Rfree_denominator                       = np.sum(abs(tmpVals))
                    total_Rfree_error                      += Rfree_numerator
                    total_Rfree_error_norm                 += Rfree_denominator
                    Rfree_complex_bybin[shellNum, iterationNum-1] = Rfree_numerator / Rfree_denominator
                Rfree_complex_total[iterationNum-1] = total_Rfree_error / total_Rfree_error_norm
            #replace Fourier components with ones from measured data from the current set of constraints
            #k[constraintInd_complex] = measuredK[constraintInd_complex]
            k[constraintInd_complex] = dt*k[constraintInd_complex] + (1-dt)*measuredK[constraintInd_complex]
            u_K = ifftn(k)
            initialObject = 2*u_K - u
            initialObject = np.real(initialObject)
            index_neg = (initialObject<0) | (support==0);            
            initialObject[index_neg]=0;
			
            u = u + initialObject - u_K
			

            #update display
            if displayFigure.DisplayFigureON:
                if iterationNum % displayFigure.displayFrequency == 0:
                    if verbose:
                        print("n_half_x = ", n_half_x)
                        print("half_window_y = ", half_window_y)
                    plt.figure(1000)
                    plt.subplot(233)
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central YZ slice")

                    plt.subplot(232)
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y, n_half_z-half_window_z:n_half_z+half_window_z]))
                    plt.title("central XZ slice")

                    plt.subplot(231)
                    plt.title("central XY slice")
                    plt.imshow(np.squeeze(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z]))

                    plt.subplot(236)
                    plt.title("YZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=0)))

                    plt.subplot(235)
                    plt.title("XZ projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=1)))

                    plt.subplot(234)
                    plt.title("XY projection")
                    plt.imshow(np.squeeze(np.sum(np.fft.fftshift(initialObject)[n_half_x-half_window_x:n_half_x+half_window_x, n_half_y-half_window_y:n_half_y+half_window_y, n_half_z-half_window_z:n_half_z+half_window_z], axis=2)))
                    plt.get_current_fig_manager().window.setGeometry(25,25,400, 400)
                    plt.draw()

                    plt.figure(2)
                    plt.get_current_fig_manager().window.setGeometry(25,450,400, 400)
                    plt.plot(range(0,numIterations),errK)
                    plt.title("K-space Error vs Iteration Number")
                    plt.xlabel("Spatial Frequency (% of Nyquist)")
                    plt.ylabel('Reciprocal Space Error')
                    plt.draw()

                    if R_freeInd_complex:
                        plt.figure(3)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,25,400, 400)
                        plt.plot(range(0,numIterations),Rfree_complex_total)
                        plt.title("Mean R-free Value vs Iteration Number")
                        plt.xlabel("Iteration Num")
                        plt.ylabel('Mean R-free')
                        plt.draw()

                        plt.figure(4)
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(450,450,400, 400)
                        X = np.linspace(0,1,np.shape(Rfree_complex_bybin)[0])
                        plt.plot(X, Rfree_complex_bybin[:,iterationNum-1])
                        plt.title("Current Rfree Value vs Spatial Frequency")
                        plt.xlabel("Spatial Frequency (% of Nyquist)")
                        plt.ylabel('Rfree')
                        plt.draw()

                    if iterationNum<numIterations:
                        ptime=1
                    else:
                        ptime=100
                    plt.pause(ptime) #forces display to update
		#end methods

        outputs['errK'] = errK
        if R_freeInd_complex:
            outputs['R_free_bybin'] = Rfree_complex_bybin
            outputs['R_free_total'] = Rfree_complex_total
        outputs['reconstruction'] = np.fft.fftshift(outputs['reconstruction'])
        if verbose:
            print("Reconstruction finished in {0:0.1f} seconds".format(time.time()-t0))
        return outputs


    def fillInFourierGrid(projections,angles,interpolationCutoffDistance, enforce_resolution_circle=True, permitMultipleGridding=True, verbose=True):
        """
        * fillInFourierGrid *

        FFT gridding function for converting a set of 2D projection images into a 3D Fourier grid

        :param projections: N x N x num_projections NumPy array containing the projections
        :param angles: 3 x num_projections NumPy array of Euler angles phi,theta, psi
        :param interpolationCutoffDistance: Radius of interpolation kernel. Only values within this radius of a grid point are considered
        :param enforce_resolution_circle: boolean; whether or not to truncate reciprocal space to Nyquist frequency
        :return: the assembled Fourier grid

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        """
        if verbose:
            print ("Assembling Fourier grid.")
        tic = time.time()
        dim1 = np.shape(projections)[0]
        dim2 = np.shape(projections)[1]
        if len(np.shape(projections))>2:
            numProjections = np.shape(projections)[2]
        else:
            numProjections = 1
        nc = np.round(dim1/2)
        n2 = nc
        measuredX = np.zeros([dim1*dim2,numProjections])
        measuredY = np.zeros([dim1*dim2,numProjections])
        measuredZ = np.zeros([dim1*dim2,numProjections])
        kMeasured = np.zeros([dim1,dim1,numProjections], dtype=complex)
        # confidenceWeights = np.zeros([dim1,dim1,numProjections])
        ky,kx = np.meshgrid(np.arange(-n2,n2,1,dtype=float),np.arange(-n2,n2,1,dtype=float))
        Q = np.sqrt(ky**2+kx**2)/n2
        kx = np.reshape(kx, [1, dim1*dim2], 'F')
        ky = np.reshape(ky, [1, dim1*dim2], 'F')
        kz = np.zeros([1, dim1*dim1])
        for projNum in range(0, numProjections):

            # convert angles to radians and construct the rotation matrix
            phi = angles[projNum, 0] * PI/180
            theta = angles[projNum, 1] * PI/180
            psi = angles[projNum, 2] * PI/180
            R = np.array([[np.cos(psi)*np.cos(theta)*np.cos(phi)-np.sin(psi)*np.sin(phi) ,np.cos(psi)*np.cos(theta)*np.sin(phi)+np.sin(psi)*np.cos(phi)   ,    -np.cos(psi)*np.sin(theta)],
            [-np.sin(psi)*np.cos(theta)*np.cos(phi)-np.cos(psi)*np.sin(phi), -np.sin(psi)*np.cos(theta)*np.sin(phi)+np.cos(psi)*np.cos(phi) ,   np.sin(psi)*np.sin(theta) ],
            [np.sin(theta)*np.cos(phi)                               , np.sin(theta)*np.sin(phi)                                ,              np.cos(theta)]])
            R = R.T

            Kcoordinates = np.zeros([3, dim1*dim2],dtype=float)
            Kcoordinates[0, :] = kx
            Kcoordinates[1, :] = ky
            Kcoordinates[2, :] = kz


            rotkCoords = np.dot(R, Kcoordinates)
            measuredX[:, projNum] = rotkCoords[0, :]
            measuredY[:, projNum] = rotkCoords[1, :]
            measuredZ[:, projNum] = rotkCoords[2, :]
            kMeasured[:, :, projNum] = fftn_fftshift(projections[:, :, projNum])

        # reorganize the coordinates and discard any flagged values
        measuredX = np.reshape(measuredX,[1, np.size(kMeasured)], 'F')
        measuredY = np.reshape(measuredY,[1, np.size(kMeasured)], 'F')
        measuredZ = np.reshape(measuredZ,[1, np.size(kMeasured)], 'F')
        kMeasured = np.reshape(kMeasured,[1, np.size(kMeasured)], 'F')
        notFlaggedIndices = kMeasured != -999
        measuredX = measuredX[notFlaggedIndices]
        measuredY = measuredY[notFlaggedIndices]
        measuredZ = measuredZ[notFlaggedIndices]
        kMeasured = kMeasured[notFlaggedIndices]

        masterInd = []
        masterVals = []
        masterDistances = []

        # check whether we need to consider multiple grid points
        if permitMultipleGridding:
            shiftMax = int(round(interpolationCutoffDistance))
        else:
            shiftMax = 0
        for Yshift in range(-shiftMax, shiftMax+1):
            for Xshift in range(-shiftMax, shiftMax+1):
                for Zshift in range(-shiftMax, shiftMax+1):

                    tmpX = np.round(measuredX) + Xshift
                    tmpY = np.round(measuredY) + Yshift
                    tmpZ = np.round(measuredZ) + Zshift

                    tmpVals = kMeasured
                    # tmpConfidenceWeights = confidenceWeights
                    distances = np.abs(measuredX-tmpX)**2 + np.abs(measuredY-tmpY)**2 + np.abs(measuredZ-tmpZ)**2
                    tmpX+=nc
                    tmpY+=nc
                    tmpZ+=nc

                    goodInd = (np.logical_not((tmpX > (dim1-1)) | (tmpX < 0) | (tmpY > (dim1-1)) | (tmpY < 0) | (tmpZ > (dim1-1)) | (tmpZ < 0))) & (distances <= (interpolationCutoffDistance**2))

                    masterInd=np.append(masterInd, np.ravel_multi_index((tmpX[goodInd].astype(np.int64), tmpY[goodInd].astype(np.int64), tmpZ[goodInd].astype(np.int64)),[dim1, dim1, dim1], order='F'))
                    masterVals=np.append(masterVals, tmpVals[goodInd])
                    masterDistances=np.append(masterDistances, distances[goodInd])


        masterInd = np.array(masterInd).astype(np.int64)
        masterVals = np.array(masterVals)
        masterDistances = np.array(masterDistances)

        #  only assemble half of the grid and then fill the remainder by Hermitian symmetry
        halfwayCutoff = ((dim1+1)**3)//2+1
        masterVals = masterVals[masterInd <= halfwayCutoff]
        masterDistances = masterDistances[masterInd <= halfwayCutoff]
        masterDistances = masterDistances +  1e-5
        masterDistances [masterDistances != 0 ]  = 1 / masterDistances[masterDistances != 0 ]
        masterInd = masterInd[masterInd <= halfwayCutoff]

        measuredK = np.zeros([dim1**3], dtype=complex)

        # accumulate the sums
        vals_real = np.bincount(masterInd, weights=(masterDistances * np.real(masterVals)))
        vals_cx = np.bincount(masterInd, weights=(masterDistances * np.imag(masterVals)))
        vals = vals_real + 1j * vals_cx
        sum_weights = np.bincount(masterInd, weights=(masterDistances))
        vals[sum_weights != 0] = vals[sum_weights != 0] / sum_weights[sum_weights != 0]
        measuredK[np.arange(np.size(vals))] = vals
        measuredK = np.reshape(measuredK,[dim1,dim1,dim1],order='F')

        measuredK[np.isnan(measuredK)] = 0

        if enforce_resolution_circle:
            Q = genfire.utility.generateKspaceIndices(measuredK)
            measuredK[Q>1] = 0

        # apply Hermitian symmetry
        measuredK = genfire.utility.hermitianSymmetrize(measuredK)

        if verbose:
            print ("Fourier grid assembled in {0:0.1f} seconds".format(time.time()-tic))
        return measuredK



    def fillInFourierGrid_DFT(projections,angles,interpolationCutoffDistance, enforce_resolution_circle, verbose=True):
        """
        * fillInFourierGrid_DFT *

        DFT gridding function for converting a set of 2D projection images into a 3D Fourier grid

        :param projections: N x N x num_projections NumPy array containing the projections
        :param angles: 3 x num_projections NumPy array of Euler angles phi,theta, psi
        :param interpolationCutoffDistance: Radius of interpolation kernel. Only values within this radius of a grid point are considered
        :param enforce_resolution_circle: boolean; whether or not to truncate reciprocal space to Nyquist frequency
        :return: the assembled Fourier grid


        Author: Yongsoo Yang
        Transcribed from MATLAB codes by Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.
        """

        if verbose:
            print ("Assembling Fourier grid.")

        tic = time.time()
        from genfire.utility import pointToPlaneClosest, pointToPlaneDistance
        (n1, n2) = (np.shape(projections)[0],np.shape(projections)[1])
        minInvThresh = 0.00001
        num_projections = np.shape(projections)[2]
        normVECs = np.zeros((num_projections,3))
        rotMATs  = np.zeros((3,3,num_projections))
        phis     = angles[:, 0] * PI/180
        thetas   = angles[:, 1] * PI/180
        psis     = angles[:, 2] * PI/180
        init_normvec = np.array([0, 0, 1],dtype=float)
        for ang_num in range(num_projections):
            phi   = phis[ang_num]
            theta = thetas[ang_num]
            psi   = psis[ang_num]
            R     = np.array([[np.cos(psi)*np.cos(theta)*np.cos(phi)-np.sin(psi)*np.sin(phi) ,np.cos(psi)*np.cos(theta)*np.sin(phi)+np.sin(psi)*np.cos(phi)   ,    -np.cos(psi)*np.sin(theta)],
            [-np.sin(psi)*np.cos(theta)*np.cos(phi)-np.cos(psi)*np.sin(phi), -np.sin(psi)*np.cos(theta)*np.sin(phi)+np.cos(psi)*np.cos(phi) ,   np.sin(psi)*np.sin(theta) ],
            [np.sin(theta)*np.cos(phi)                               , np.sin(theta)*np.sin(phi)                                ,              np.cos(theta)]])
            rotMATs[:, :, ang_num] = R.T
            normVECs[ang_num, :] = np.dot(R.T, init_normvec.T)
        k1               = np.arange(-1*(n1//2), 1, 1, dtype=float)
        k1_full          = np.arange(-1*(n1//2), n1//2 + 1, 1, dtype=float)
        k2               = np.arange(-1 * n2//2, n2//2 + 1, 1, dtype=float)
        k3               = np.arange(-1 * n1//2, n1//2 + 1, 1, dtype=float)
        (null, K1, null) = np.meshgrid(k2, k1, k3)
        FS               = np.zeros_like(K1, dtype=complex)
        Numpt            = np.zeros_like(K1)
        invSumTotWeight  = np.zeros_like(K1, dtype=float)
        [K20, K10] = np.meshgrid(k2[:-1],k1_full[:-1])
        K20 = K20.flatten()
        K10 = K10.flatten()
        try:
            artifical_error = 1/0 # This loop uses broadcasting, which can use more memory, so there is a try/catch as a failsafe. However
            # the simple loop seems to be faster, so for the moment I have just introduced an error artificially as a lazy way of leaving both implementations
            for proj_num in range(num_projections):
                curr_proj = projections[:, :, proj_num].flatten()
                [K2, K1, K3] = np.meshgrid(k2,k1,k3)
                D = pointToPlaneDistance(np.vstack((K1.flatten(order="F"), K2.flatten(order="F"), K3.flatten(order="F"))).T, normVECs[proj_num,:])
                Dind = np.array(np.where(D < interpolationCutoffDistance))
                CP = pointToPlaneClosest(np.vstack((K1.flatten(order="F")[[Dind]], K2.flatten(order="F")[[Dind]], K3.flatten(order="F")[[Dind]])).T, normVECs[proj_num,:].T,np.zeros(np.size(Dind),dtype=float))
                CP_plane = np.dot(np.linalg.inv(rotMATs[:, :, proj_num]), CP.T)

                Gind = Dind[0,(abs(CP_plane[0,:]) <= n1/2) & (abs(CP_plane[1,:]) <= n2/2)]
                G_CP_plane = CP_plane[:,( abs(CP_plane[0,:]) <= n1/2 )& (abs(CP_plane[1,:]) <= n2/2) ]
                nonzero_ind = np.where(curr_proj!=0)
                X = np.zeros((np.shape(G_CP_plane)[1], 1), dtype=float)
                Y = np.zeros((np.shape(G_CP_plane)[1], 1), dtype=float)
                X[:, 0] = G_CP_plane[0, :]
                Y[:, 0] = G_CP_plane[1, :]

                Fpoints = np.sum( curr_proj[nonzero_ind] * np.exp( -1j*2*PI * (K10[nonzero_ind] * X / n1 + K20[nonzero_ind] * Y / n2  ) ) ,axis=1)
                distances = D[Gind]
                distances[ distances < minInvThresh ] = minInvThresh
                currTotWeight = 1 / distances
                Gind = np.unravel_index(Gind, np.shape(FS), order="F")
                FS[Gind] = FS[Gind] * invSumTotWeight[Gind] + currTotWeight * Fpoints
                invSumTotWeight[Gind] = invSumTotWeight[Gind] + currTotWeight
                FS[Gind] = FS[Gind] / invSumTotWeight[Gind]
                Numpt[Gind] = Numpt[Gind] + 1
        except:
            for proj_num in range(num_projections):
                curr_proj = projections[:, :, proj_num].flatten()
                [K2, K1, K3] = np.meshgrid(k2,k1,k3)
                D = pointToPlaneDistance(np.vstack((K1.flatten(order="F"), K2.flatten(order="F"), K3.flatten(order="F"))).T, normVECs[proj_num,:])
                Dind = np.array(np.where(D < interpolationCutoffDistance))
                CP = pointToPlaneClosest(np.vstack((K1.flatten(order="F")[[Dind]], K2.flatten(order="F")[[Dind]], K3.flatten(order="F")[[Dind]])).T, normVECs[proj_num,:].T,np.zeros(np.size(Dind),dtype=float))
                CP_plane = np.dot(np.linalg.inv(rotMATs[:, :, proj_num]), CP.T)

                Gind = Dind[0,(abs(CP_plane[0,:]) <= n1/2) & (abs(CP_plane[1,:]) <= n2/2)]
                G_CP_plane = CP_plane[:,( abs(CP_plane[0,:]) <= n1/2 )& (abs(CP_plane[1,:]) <= n2/2) ]
                Fpoints = np.zeros(np.shape(G_CP_plane)[1], dtype=complex)

                nonzero_ind = np.where(curr_proj!=0)
                # for i,v in enumerate(G_CP_plane.T):
                #     Fpoints[i] = np.sum( curr_proj[nonzero_ind] * np.exp( -1j*2*PI * (K10[nonzero_ind] * v[0] / n1 + K20[nonzero_ind] * v[1] / n2  ) ) )


                K10_t = K10[nonzero_ind]
                K20_t = K20[nonzero_ind]
                curr_proj = curr_proj[nonzero_ind]

                for i in range(np.shape(G_CP_plane)[1]):
                    Fpoints[i] = np.sum( curr_proj * np.exp( -1j*2*PI * (K10_t * G_CP_plane[0, i] / n1 + K20_t * G_CP_plane[1, i] / n2  ) ) )
                    # Fpoints[i] = np.sum( curr_proj[nonzero_ind] * np.exp( -1j*2*PI * (K10[nonzero_ind] * G_CP_plane[0, i] / n1 + K20[nonzero_ind] * G_CP_plane[1, i] / n2  ) ) )
                distances = D[Gind]
                distances[ distances < minInvThresh ] = minInvThresh
                currTotWeight = 1 / distances
                Gind = np.unravel_index(Gind, np.shape(FS), order="F")
                FS[Gind] = FS[Gind] * invSumTotWeight[Gind] + currTotWeight * Fpoints
                invSumTotWeight[Gind] = invSumTotWeight[Gind] + currTotWeight
                FS[Gind] = FS[Gind] / invSumTotWeight[Gind]
                Numpt[Gind] = Numpt[Gind] + 1
        # measuredK = np.zeros((n1,n2,n1), dtype=complex)
        measuredK = np.zeros((n1+1,n2+1,n1+1), dtype=complex)
        measuredK[:n1//2 + 1, :, :] = FS[:, :, :]
        if verbose:
            print ("Fourier grid assembled in {0:0.1f} seconds".format(time.time()-tic))

        if enforce_resolution_circle:
            Q = genfire.utility.generateKspaceIndices(measuredK)
            measuredK[Q>1] = 0

        return genfire.utility.hermitianSymmetrize(measuredK)[:-1,:-1,:-1]

    def readMAT(filename):
        """
        * readMAT *

        Read projections from a .mat file

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: MATLAB file (.mat) containing projections
        :return: NumPy array containing projections
        """

        try: #try to open the projections as a stack
            projections = scipy.io.loadmat(filename)
            projections = np.array(projections[projections.keys()[0]])
        except: ##
             #check if the projections are in individual files
            flag = True
            filename_base, file_extension = os.path.splitext(filename)
            projectionCount = 1
            while flag: #first count the number of projections so the array can be initialized
                projectionCount = projectionCount
                nextFile = filename_base + str(projectionCount) + file_extension
                if os.path.isfile(nextFile):
                    projectionCount += 1
                else:
                    flag = False


            ## open first projection to get dimensions
            pj = scipy.io.loadmat(filename_base + str(1) + file_extension)
            pj = pj[projections.keys()[0]]
            dims = np.shape(pj)
            #initialize projection array
            projections = np.zeros((dims[0], dims[1], projectionCount),dtype=int)

            #now actually load in the tiff images
            for projNum in range(projectionCount):
                nextFile = filename_base + str(projNum) + file_extension
                pj = scipy.io.loadmat(filename_base + str(projNum) + file_extension)
                pj = pj[pj.keys()[0]]
                projections[:, :, projNum] = np.array(pj)

        return projections


    def readTIFF(filename):
        """
        * readTIFF *

        Read (possibly multiple) TIFF images into a NumPy array

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: Name of TIFF file or TIFF file basename to read. If the filename is a base then
        #       the images must begin with the string contained in filename followed by consecutive integers with
        #       no zero padding, i.e. foo1.tiff, foo2.tiff,..., foo275.tiff
        :return: NumPy array containing projections
        """
        import functools
        from PIL import Image
        import os
        try:
            projections = np.array(Image.open(filename))
        except:
            flag = True
            filename_base, file_extension = os.path.splitext(filename)
            projectionCount = 1
            while flag: #first count the number of projections so the array can be initialized
                projectionCount = projectionCount
                nextFile = filename_base + str(projectionCount) + file_extension
                if os.path.isfile(nextFile):
                    projectionCount += 1
                else:
                    flag = False

            ## open first projection to get dimensions
            dims = np.shape(Image.open(filename_base + str(1) + file_extension))

            #initialize projection array
            projections = np.zeros((dims[0], dims[1], projectionCount),dtype=int)

            pool = Pool(4)
            func = functools.partial(readInTiffProjection, filename_base)
            pj = pool.map(func, range(projectionCount))
            for j  in range(projectionCount):
                projections[:, :, j] = pj[j]
            return projections

    def readInTiffProjection(filename_base, fileNumber):
        """
        * readInTiffProjection *

        Reads and returns a single TIFF image as a NumPy array

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename_base: Base filename of TIFF
        :param fileNumber: Image number
        :return: Image in a 2D NumPy array
        """
        from PIL import Image
        nextFile = filename_base + str(fileNumber) + '.tif'
        return np.array(Image.open(nextFile))

    def readMRC(filename, dtype=float,order="C"):
        """
        * readMRC *

        Read in a volume in .mrc file format. See http://bio3d.colorado.edu/imod/doc/mrc_format.txt

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.

        :param filename: Filename of .mrc
        :return: NumPy array containing the .mrc data
        """
        import struct
        headerIntNumber = 56
        sizeof_int = 4
        headerCharNumber = 800
        sizeof_char = 1
        with open(filename,'rb') as fid:
            int_header = struct.unpack('=' + 'i'*headerIntNumber, fid.read(headerIntNumber * sizeof_int))
            char_header = struct.unpack('=' + 'c'*headerCharNumber, fid.read(headerCharNumber * sizeof_char))
            dimx, dimy, dimz, data_flag= int_header[:4]
            if (data_flag == 0):
                datatype='u1'
            elif (data_flag ==1):
                datatype='i1'
            elif (data_flag ==2):
                datatype='f4'
            elif (data_flag ==3):
                datatype='c'
            elif (data_flag ==4):
                datatype='f4'
            elif (data_flag ==6):
                datatype='u2'
            else:
                raise ValueError("No supported datatype found!\n")
            return np.fromfile(file=fid, dtype=datatype,count=dimx*dimy*dimz).reshape((dimx,dimy,dimz),order=order).astype(dtype)

    def writeMRC(filename, arr, datatype='f4'):
        """
        * writeMRC *

        Write a volume to .mrc file format. See http://bio3d.colorado.edu/imod/doc/mrc_format.txt

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved

        :param filename: Filename of .mrc file to write
        :param arr: NumPy volume of data to write
        :param dtype: Type of data to write
        """
        dimx, dimy, dimz = np.shape(arr)
        if datatype != arr.dtype:
            arr = arr.astype(datatype)
        int_header = np.zeros(56,dtype='int32')

        if (datatype == 'u1'):
            data_flag = 0
        elif (datatype =='i1'):
            data_flag = 1
        elif (datatype =='f4'):
            data_flag = 2
        elif (datatype =='c'):
            data_flag = 3
        elif (datatype =='f4'):
            data_flag = 4
        elif (datatype =='u2'):
            data_flag = 6
        else:
            raise ValueError("No supported datatype found!\n")

        int_header[:4] = (dimx,dimy,dimz,data_flag)
        char_header = str(' '*800)
        with open(filename,'wb') as fid:
            fid.write(int_header.tobytes())
            fid.write(char_header)
            fid.write(arr.tobytes())



    class DisplayFigure:
        """
        * DisplayFigure *

        Helper class for displaying figures during reconstruction process

        Author: Alan (AJ) Pryor, Jr.
        Jianwei (John) Miao Coherent Imaging Group
        University of California, Los Angeles
        Copyright 2015-2016. All rights reserved.
        """
        def __init__(self):
            self.DisplayFigureON = False
            self.DisplayErrorFigureON = False
            self.displayFrequency = 5
            self.reconstructionDisplayWindowSize = 0


def toString(string):
    try:
        import genfire.gui.utility
        return genfire.gui.utility.toString(string)
    except ImportError:
        return str(string)

class ReconstructionParameters():

    """
    Helper class for containing reconstruction parameters
    """
    _supportedFiletypes = ['.tif', '.mrc', '.mat', '.npy']
    _supportedAngleFiletypes = ['.txt', '.mat', '.npy']
    def __init__(self):
        self.projections                         = ""
        self.eulerAngles                         = ""
        self.support                             = ""
        self.resolutionExtensionSuppressionState = 2 #1 for resolution extension/suppression, 2 for off, 3 for just extension
        self.methodState = 1 #1 for ER, 2 for DR
        self.numIterations                       = 100
        self.displayFigure                       = DisplayFigure()
        self.oversamplingRatio                   = 3
        self.interpolationCutoffDistance         = 0.7
        self.isInitialObjectDefined              = False
        self.resultsFilename                     = os.path.join(os.getcwd(), 'results.mrc')
        self.useDefaultSupport                   = True
        self.calculateRfree                      = True
        self.initial                             = None
        self.constraintPositivity                = True
        self.constraintSupport                   = True
        self.griddingMethod                      = "FFT"
        self.enforceResolutionCircle             = True
        self.permitMultipleGridding              = True
        self.verbose                             = True

    def checkParameters(self): #verify file extensions are supported
        import os
        parametersAreGood = 1

        projection_extension = os.path.splitext(self.projections)
        if projection_extension[1] not in ReconstructionParameters._supportedFiletypes \
                or not os.path.isfile(self.projections):
            parametersAreGood = 0

        angle_extension = os.path.splitext(self.eulerAngles)
        if angle_extension[1] not in ReconstructionParameters._supportedAngleFiletypes \
                or not os.path.isfile(self.eulerAngles):
            parametersAreGood = 0

        if not self.useDefaultSupport:
            if self.support != "": #empty support filename is okay, as this will trigger generation of a default support
                support_extension = os.path.splitext(self.support)
                if support_extension[1] not in ReconstructionParameters._supportedFiletypes \
                        or not os.path.isfile(self.support):
                    parametersAreGood = 0

        if not self.getResultsFilename():
            parametersAreGood = 0
        return parametersAreGood

    # Define setters/getters. It's not very pythonic to do so, but  I came from C++ and wrote
    # this before I knew better. In any case it doesn't affect much.

    def setProjectionFilename(self, projections):
        if projections:
            self.projections = os.path.join(os.getcwd(), toString(projections))

    def getProjectionFilename(self):
        return self.projections

    def setAngleFilename(self, eulerAngles):
        if eulerAngles:
            self.eulerAngles = os.path.join(os.getcwd(), toString(eulerAngles))

    def getAngleFilename(self):
        return self.eulerAngles

    def setSupportFilename(self, support):
        if support:
            self.support = os.path.join(os.getcwd(), toString(support))

    def getSupportFilename(self):
        return self.support

    def setResultsFilename(self, resultsFilename):
        if resultsFilename:
            self.resultsFilename = os.path.join(os.getcwd(), toString(resultsFilename))

    def getResultsFilename(self):
        return self.resultsFilename

    def setInitialObjectFilename(self, initialObject):
        self.initialObject = os.path.join(os.getcwd(), toString(initialObject))
        self.isInitialObjectDefined = True

    def getInitialObjectFilename(self):
        if self.CheckIfInitialObjectIsDefined():
            return self.initialObject
        else:
            pass

    def CheckIfInitialObjectIsDefined(self):
        return self.isInitialObjectDefined

    def setResolutionExtensionSuppressionState(self, state):
        self.resolutionExtensionSuppressionState = state

    def getResolutionExtensionSuppressionState(self):
        return self.resolutionExtensionSuppressionState

    def setMethodState(self, state):
        self.methodState = state

    def getMethodState(self):
        return self.methodState

    def setNumberOfIterations(self,numIterations):
        self.numIterations = numIterations

    def getNumberOfIterations(self):
        return self.numIterations

    def toggleDisplayFigure(self): # whether or not to display figure during reconstruction
        if self.displayFigure.DisplayFigureON:
            self.displayFigure.DisplayFigureON = False
        else:
            self.displayFigure.DisplayFigureON = True

        if self.displayFigure.DisplayErrorFigureON:
            self.displayFigure.DisplayErrorFigureON = False
        else:
            self.displayFigure.DisplayErrorFigureON = True

    def getDisplayFigure(self):
        return self.displayFigure

    def setOversamplingRatio(self, oversamplingRatio):
        self.oversamplingRatio = int(oversamplingRatio)

    def getOversamplingRatio(self):
        return self.oversamplingRatio

    def setInterpolationCutoffDistance(self, interpolationCutoffDistance):
        self.interpolationCutoffDistance = float(interpolationCutoffDistance)

    def getInterpolationCutoffDistance(self):
        return self.interpolationCutoffDistance

class GenfireReconstructor():
    """
    Primary class for running GENFIRE Reconstructions
    """
    def __init__(self, projections="", eulerAngles="", support="", initialObject=None,
                 resultsFilename=os.path.join(os.getcwd(), 'results.mrc'), resolutionExtensionSuppressionState=1, 
                 numIterations=100, oversamplingRatio=3, interpolationCutoffDistance=0.7, useDefaultSupport=True,
                 calculateRfree=True, constraintPositivity=True, constraintSupport=True, griddingMethod="FFT",
                 enforceResolutionCircle=True, permitMultipleGridding=True, methodState=1, verbose=True):

        """
        :param projections: (string or numpy.ndarray) file containing projections or numpy array with projections
        :param eulerAngles: (string or numpy.ndarray) file containing Euler angles or numpy array with Euler angles
        :param support: (string or numpy.ndarray) file containing support or numpy array with support
        :param resultsFilename: (string or numpy.ndarray) file in which to store reconstruction volume
        :param initialObject: (string or numpy.ndarray) (optional) filename containing intial object or numpy array with initial object
        :param resolutionExtensionSuppressionState: (int) 1: use resolution extension/suppression;
        2: do not use; 3: extension only
        :param numIterations: (int) number of GENFIRE iterations
        :param oversamplingRatio: (int) oversampling ratio; determines how much zero-padding is applied prior to
         gridding
        :param interpolationCutoffDistance: (float) distance in pixels within which to consider data for gridding
        :param useDefaultSupport: (bool) create a default support; defined as a cube with dimensions identical to
         input projections
        :param calculateRfree: (bool) whether or not to compute Rfree
        :param constraintPositivity: (bool) whether to enforce positivity constraint
        :param constraintSupport: (bool) whether to enforce support constraint
        :param griddingMethod: (string) "FFT" or "DFT"
        :param enforceResolutionCircle: (bool) whether to limit gridded data to within Nyquist frequency
        :param permitMultipleGridding: (bool) whether to allow a given measured datapoint to be included in calculation
         of multiple Fourier grid points
        :param verbose: (bool) prints additional information about the reconstruction
        """

        self.reconstruction_ = None
        self.errK_ = None
        self.R_free_bybin_ = None
        self.R_free_total_ = None

        self.params = ReconstructionParameters()
        self.params.projections = projections
        self.params.eulerAngles = eulerAngles
        self.params.support = support
        self.params.resultsFilename = resultsFilename
        self.params.resolutionExtensionSuppressionState = resolutionExtensionSuppressionState #1 for resolution extension/suppression, 2 for off, 3 for just extension
        self.params.methodState = methodState		#1 for ER, 2 for DR
        self.params.numIterations = numIterations
        self.params.oversamplingRatio = oversamplingRatio
        self.params.interpolationCutoffDistance = interpolationCutoffDistance
        self.params.isInitialObjectDefined = False
        self.params.useDefaultSupport = useDefaultSupport
        self.params.calculateRfree = calculateRfree
        self.params.initialObject = initialObject
        self.params.constraintPositivity = constraintPositivity
        self.params.constraintSupport = constraintSupport
        self.params.griddingMethod = griddingMethod
        self.params.enforceResolutionCircle = enforceResolutionCircle
        self.params.permitMultipleGridding = permitMultipleGridding
        self.params.verbose = verbose

    def printGenfire(self):
        print("""
       ______  ________  ____  _____  ________  _____  _______     ________
     .' ___  ||_   __  ||_   \|_   _||_   __  ||_   _||_   __ \   |_   __  |
    / .'   \_|  | |_ \_|  |   \ | |    | |_ \_|  | |    | |__) |    | |_ \_|
    | |   ____  |  _| _   | |\ \| |    |  _|     | |    |  __ /     |  _| _
    \ `.___]  |_| |__/ | _| |_\   |_  _| |_     _| |_  _| |  \ \_  _| |__/ |
     `._____.'|________||_____|\____||_____|   |_____||____| |___||________|

        """)

    def printParams(self):
        from genfire.utility import printStringOrNumpyArray
        printStringOrNumpyArray(self.params.projections, 'Projections')
        printStringOrNumpyArray(self.params.eulerAngles, 'Euler angles')
        printStringOrNumpyArray(self.params.support, 'Support')
        printStringOrNumpyArray(self.params.initialObject, 'Initial Object')
        print("resultsFilename = {}".format(self.params.resultsFilename))
        print("griddingMethod = {}".format(self.params.griddingMethod))
        print("resolutionExtensionSuppressionState = {}".format(self.params.resolutionExtensionSuppressionState))
        print("methodState = {}".format(self.params.methodState))
        print("numIterations = {}".format(self.params.numIterations))
        print("oversamplingRatio = {}".format(self.params.oversamplingRatio))
        print("interpolationCutoffDistance = {}".format(self.params.interpolationCutoffDistance))
        print("useDefaultSupport = {}".format(self.params.useDefaultSupport))
        print("calculateRfree = {}".format(self.params.calculateRfree))
        print("constraintPositivity = {}".format(self.params.constraintPositivity))
        print("constraintSupport = {}".format(self.params.constraintSupport))
        print("enforceResolutionCircle = {}".format(self.params.enforceResolutionCircle))
        print("permitMultipleGridding = {}".format(self.params.permitMultipleGridding))

    def reconstruct(self):
        if self.params.verbose:
            self.printGenfire()
            self.printParams()

        # Handle parameters that can be either passed as a filename or a numpy array
        if isinstance(self.params.projections, str):
            projections = genfire.fileio.loadProjections(self.params.projections) # load projections into a 3D numpy array
        else:
            projections = self.params.projections

        if isinstance(self.params.eulerAngles, str):
            eulerAngles = genfire.fileio.loadAngles(self.params.eulerAngles)
        else:
            eulerAngles = self.params.eulerAngles

        # Do a check of validity of Euler angle input
        if np.shape(eulerAngles)[1] > 3:
                raise ValueError("Error! Dimension of angles incorrect.")
        if np.shape(eulerAngles)[1] == 1:
            tmp = np.zeros([np.shape(eulerAngles)[1], 3])
            tmp[1, :] = eulerAngles
            angles = tmp
            del tmp

        # get dimensions of array and determine the array size after padding
        dims = np.shape(projections)
        paddedDim = dims[0] * self.params.oversamplingRatio
        padding = int((paddedDim-dims[0])/2)

        # load the support, or generate one if none was provided
        if (self.params.useDefaultSupport or self.params.support == ""):
            support = np.ones((dims[0],dims[0],dims[0]),dtype=float)
        elif isinstance(self.params.support, str):
            support = (genfire.fileio.readVolume(self.params.support) != 0).astype(bool)
        else:
            support = self.params.support

        # now zero-pad to match the oversampling ratio
        support = np.pad(support,((padding,padding),(padding,padding),(padding,padding)),'constant')
        projections = np.pad(projections,((padding,padding),(padding,padding),(0,0)),'constant')

        #load initial object, or initialize it to zeros if none was given
        if isinstance(self.params.initialObject, np.ndarray):
            initialObject = self.params.initialObject
        else:
            if self.params.initialObject is not None and os.path.isfile(self.params.initialObject):
                initialObject = genfire.fileio.readVolume(self.params.initialObject)
                initialObject = np.pad(initialObject,((padding,padding),(padding,padding),(padding,padding)),'constant')
            else:
                initialObject = np.zeros_like(support)
                
        # grid the projections
        if self.params.griddingMethod == "DFT":
            measuredK = genfire.reconstruct.fillInFourierGrid_DFT(projections,
                                                                  eulerAngles,
                                                                  self.params.interpolationCutoffDistance,
                                                                  self.params.enforceResolutionCircle,
                                                                  self.params.verbose)
        else:
            measuredK = genfire.reconstruct.fillInFourierGrid(projections,
                                                              eulerAngles,
                                                              self.params.interpolationCutoffDistance,
                                                              self.params.enforceResolutionCircle,
                                                              self.params.permitMultipleGridding,
                                                              self.params.verbose)

        measuredK = np.fft.ifftshift(measuredK)

        # create a map of the spatial frequency to be used to control resolution extension/suppression behavior
        K_indices = genfire.utility.generateKspaceIndices(support)
        K_indices = np.fft.fftshift(K_indices)
        resolutionIndicators = np.zeros_like(K_indices)
        resolutionIndicators[measuredK != 0] = 1-K_indices[measuredK != 0]

        # if calculating Rfree, setup some infrastructure
        if self.params.calculateRfree:
            R_freeInd_complexX = []
            R_freeInd_complexY = []
            R_freeInd_complexZ = []
            R_freeVals_complex = []
            shell_thickness_pixels = 1 # pixel thickness of an individual shell of Rfree points
            numberOfBins = int(round(dims[0]/2/shell_thickness_pixels)) # number of frequency bins. Rfree will be tracked within each shell separately
            percentValuesForRfree = 0.05 # percentage of measured points to withhold
            spatialFrequencyForRfree = np.linspace(0,1,numberOfBins+1)
            K_indicesSmall =(K_indices)[:, :, 0:(np.shape(measuredK)[-1]//2+1)]

            for shellNum in range(0,numberOfBins):
                # collect relevant points
                measuredPointInd_complex = np.where((measuredK[:, :, 0:(np.shape(measuredK)[-1]//2+1)] != 0) & (K_indicesSmall>=(spatialFrequencyForRfree[shellNum])) & (K_indicesSmall<=(spatialFrequencyForRfree[shellNum+1])))

                # randomly shuffle
                shuffledPoints = np.random.permutation(np.shape(measuredPointInd_complex)[1])
                measuredPointInd_complex = (measuredPointInd_complex[0][shuffledPoints], measuredPointInd_complex[1][shuffledPoints], measuredPointInd_complex[2][shuffledPoints])

                # determine how many values to take
                cutoffInd_complex = np.floor(np.shape(measuredPointInd_complex)[1] * percentValuesForRfree).astype(int)

                # collect the Rfree values and coordinates
                R_freeInd_complexX.append(measuredPointInd_complex[0][:cutoffInd_complex])
                R_freeInd_complexY.append(measuredPointInd_complex[1][:cutoffInd_complex])
                R_freeInd_complexZ.append(measuredPointInd_complex[2][:cutoffInd_complex])
                R_freeVals_complex.append(measuredK[R_freeInd_complexX[shellNum], R_freeInd_complexY[shellNum], R_freeInd_complexZ[shellNum] ])

                # delete the points from the measured data
                measuredK[R_freeInd_complexX[shellNum], R_freeInd_complexY[shellNum], R_freeInd_complexZ[shellNum]] = 0

            # create tuple of coordinates
            R_freeInd_complex = [[R_freeInd_complexX], [R_freeInd_complexY], [R_freeInd_complexZ]]
            del R_freeInd_complexX
            del R_freeInd_complexY
            del R_freeInd_complexZ
        else:
            R_freeInd_complex = []
            R_freeVals_complex = []

        if self.params.resolutionExtensionSuppressionState==1: # resolution extension/suppression
            constraintEnforcementDelayIndicators = np.array(np.concatenate((np.arange(0.95, -.25, -0.15), np.arange(-0.15, .95, .1)), axis=0))
        elif self.params.resolutionExtensionSuppressionState==2:# no resolution extension or suppression
            constraintEnforcementDelayIndicators = np.array([-999, -999, -999, -999])
        elif self.params.resolutionExtensionSuppressionState==3:# resolution extension only
            constraintEnforcementDelayIndicators = np.concatenate((np.arange(0.95, -.15, -0.15),[-0.15, -0.15, -0.15]))
        else:
            if self.params.verbose:
                print("Warning! Input resolutionExtensionSuppressionState does not match an available option. Deactivating dynamic constraint enforcement and continuing.\n")
                constraintEnforcementDelayIndicators = np.array([-999, -999, -999, -999])


        results = reconstruct(self.params.numIterations,
                              np.fft.fftshift(initialObject),
                              np.fft.fftshift(support),
                              (measuredK)[:, :, 0:(np.shape(measuredK)[-1] // 2 + 1)],
                              (resolutionIndicators)[:, :, 0:(np.shape(measuredK)[-1] // 2 + 1)],
                              constraintEnforcementDelayIndicators,
                              R_freeInd_complex,
                              R_freeVals_complex,
                              self.params.displayFigure,
                              self.params.constraintPositivity,
                              self.params.constraintSupport,
                              self.params.methodState,
                              self.params.verbose)
        ncBig = paddedDim//2
        n2 = dims[0]//2
        results['reconstruction'] = results['reconstruction'][ncBig-n2:ncBig+n2,ncBig-n2:ncBig+n2,ncBig-n2:ncBig+n2]
        return results
        # self.reconstruction_ = results['reconstruction']
        # self.errK_ = results['R_free_bybin']
        # if "R_freeInd_complex" in results.keys():
        #     self.R_free_bybin_ = results['R_free_bybin']
        #     self.R_free_total_ = results['R_free_total']

