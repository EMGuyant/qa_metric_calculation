# QA Metric Calculation
QAData - Python program for processing raw input data files and produces an output file containing various Quality Assurance measures. This project was completed as
part of a Python course, and is not maintained.

## PROGRAM DESCRIPTION:
   Program takes an input CSV file (raw data input rigid format) creates a dataframe of data, splits the
   Spike and Duplicate ";" delimiated string values and generates a corresponding list of 
   values to be used for QA calculations. For each record in the input file a instance of 
   the QA class is created and the Spike/Duplicate value is assigned, and the known spiking concentration, percent recovery, and relative percent difference are all calculated. After calculation of QA metrics a determination is made for each item on whether it passes or fails specific QA limits. Finally an outputs CSV is created containing the item ID, Spike Recovery, Spike Pass/Fail, Duplicate Recovery, Duplicate Pass/Fail, Relative Percent Difference (spike/duplicate), and RPD Pass/Fail. A QA summary is then
   displayed on the user interface, and the user can view the output file or exit the program.

## USAGE:
1) import QAData
2) QAData.process_data() - Opens user interface window. The interface guides user through Input, Output, and Process Data steps.

UserInterface Steps
1) Click "Select Input File" and navigate to and select input file
2) Click "Select Output File" and navigate to where you would like the output file save and add or accept default
3) Click "Process QA Data" - QA Summary will appear on the bottom of the the interface window
4) Click "Open Output File" to view the output CSV file
5) Click "Exit" to end the program

## INPUT FILE:
Program read an input CSV file contianing the ID(value), Original Sample(value), Spike Sample(";" deliminated string), and Spike Duplicate Sample(";" deliminated string) and the measured value.
* ID - Unique Identifier for the record
* Original - Measure value of original sample
* Spike - String required value for QA calculations 
(ID;ConcentrateConcentration;AliquotVolume;TotalVolume;MeasureValue)
* Duplicate - String required value for QA calculations 
(ID;ConcentrateConcentration;AliquotVolume;TotalVolume MeasureValue)
* Example file Infile.csv provided

## OUTPUT FILE:
Program generates an output CSV file containing the ID, Spike Percent Recovery, Spike Pass/Fail, Duplicate Percent Recovery, Duplicate Pass/Fail, Relative Percent Differenct (spike/duplicate), and Relative Percent Difference Pass/Fail. Example file DefaultOutputFileName.csv provided

## DESIGN:
### QAData(): 
Main function of the program. Creates the user interface window and calls all other functions required to move from input data to output file. Adds new buttons after each input step to guide user along and then after processing data adds new ending options to open the output or exit the program.
   
### getClickLocation(w, input_output): 
Through various steps in the program the user must interact with the interface window. getClickLocation gets the mouse click X,Y and passes these value to another fucntion to detemine which action "button" was clicked on and returns the name of the button. Two arguments the active graphics window, and a string of whether the program is showing input buttons or output
buttons. Contains a while loop which continues to wait for a mouse click if X,Y do not correspond to one of the interface buttons.
   
### buttonClick(x, y, input_output): 
Nested if loops with the X,Y coordinates of all interface buttons, dependent on the input_output string and the X,Y of a mouse click, the function returns the name of the 
button clicked.The name of the button returned drives the logical steps of the main funciton.
   
### inputSelection(): 
Prompts user to select the input file and assigns its name to the variable infileName.This function is called if buttonClick (1st time) returns a value of 'input'. Calls the function verifyFileSelection.
   
### outputSelection(): 
Prompts user to select the location and file name of the output file and assigns it to the variable outfileName. This function is called if buttonClick returns a value of 'input' (2nd time). Calls the function verifyFileSelection.

### verifyFileSelection(fileName): 
Since both input/output file are required for the program to funciton properly this verifys that a file has been selected (i.e. fileName is not empty string).
   
### processData(infileName, outfileName): 
Sequentially calls the functions to first process the input data (split Spike/Duplicate strings) and asssigns the input dataframe to rawData. Second calls function which produces the output dataframe, and then writes the output CSV file. This function returns the output dataframe for additional use creating the QA Summary. This function is called if buttonClick returns a value of 'input (3rd time).

### processInput(infileName): 
Read the input CSV to a dataframe. Splits the Spike and Duplicate string by the deliminator ";" creating a list of values. Returns the rawData dataframe.
   
### generateOutData(rawData): 
Creates and empty outData dataframe with assigned column headers. Iterates over the rawData dataframe, and for each row defines the qaID as the ID of the input and initializes an instances of the QA class. Appends the ID, and QA calculations defined in the QA class to the outData dataframe. Returns outData.
### class QA:

#### `__init__(self, rowData)`: 
Initializes QA instance with current row of data of iteration in generateOutData.
         
##### Data: 
Instance variable for the row of Data
	 
##### Spike/Duplicate: 
Instance variable of the Spike measured value Index 2/3 of Data and index 4 of list of values spike/dupConc: Instance variable of the known spiking concentration (calls the Concentration method)
   	 
##### spike/dupRecovery: 
Instance variable of the percent recovery (calls the Recovery method)

##### spike/dupPassFail: 
Pass/Fail determination of set QA limits (calls the PassFail method)

##### RPD: 
Instance variable of the relative percent difference betweent the Spike and Duplicate measured values

##### RPDPassFail: 
Pass/Fail determination of RPD limit

#### `Concentration(self, concentrate, aliquot, volume)`: 
Method that calculates and returns the spiking concentration arguments are Index 2 (spike) or 3 (duplicate) of Data and Index 1, 2, and 3 of each list respectively.
      
#### `Recovery(self, original, spike, concentration)`: 
Method that calcuates and returns the percent recovery arguments are all defined as previous instance variables.
      
#### `PassFail(self, qaMeasure, rpd=False)`: 
Method that determines if the percent recoveries and RPD are within specificed limits. Arguments are the QA measure to be tested (Spike Recovery, Duplicate Recovery, or RPD), and when the RPD is passed a the qaMeasure the option argument rpd=True this is due to RPD having different QA limit that the recovery. Series of get... method that return the value of the instance variables used to build the output.
   
### class FailedSummary:
#### `__init___(self, data, measure)`: 
Initializes FailedSummary instance with the output dataframe.

##### totalItems: 
Instance variable of the total count of records in the dataframe
         
##### failedItems: 
Instance variable of the count of items that failed QA (measure outside of limits)

##### percentFailed: 
Instance variable of the percentage of total that failed
