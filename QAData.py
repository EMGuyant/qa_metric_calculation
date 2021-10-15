#Description of Program - Quality Assurance Measurments of Raw Data Input file
#--------------------------------------------------------------------------------------------------
#Program takes an input CSV file (raw data input) creates a dataframe of data, splits the
#   Spike and Duplicate ";" delimiated string values and generates a corresponding list of 
#   values to be used for QA calculations. For each record in the input file a instance of 
#   the QA class is created and the Spike/Duplicate value is assigned, and the know spiking
#   concentration, percent recovery, and relative percent difference are all calculated.
#   After calculation of QA metrics a determination is made for each item on whether it 
#   passes or fails specific QA limits. Finally an outputs CSV is created containing the 
#   item ID, Spike Recovery, Spike Pass/Fail, Duplicate Recovery, Duplicate Pass/Fail, 
#   Relative Percent Difference (spike and duplicate), and RPD Pass/Fail.
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
import pandas #Input/Output processing
from os import startfile #Handles option of open Output CSV file
from graphics import * #Summary Window after Export
#import tkinter dialogs for selecting input and creating output files
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
#hide tkinter.Tk main window
Tk().wm_withdraw()
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def process_data():
    """Program main function. Generates user interface to select input/output files, generate 
    output data, view summary of QA metrics, and provides option to open CSV export file """
    print("PROCESS QUALITY ASSURANCE DATA")
    #User interface window creation
    win = GraphWin("Quality Assurance Data Processing", 400, 440, False)
    message = Text(Point(200,10), "Quality Assurance Data Processing")
    message.draw(win)

    #Draw Input File "Button"
    inputButton = Text(Point(200,70), "Select Input File").draw(win)
    Rect = Rectangle(Point(120,50), Point(280,90)).draw(win)
    #User Instruction
    print('\nClick "Select Input File" and navigate to and Select the Input file.')
    #Get X/Y of mouse click and check if within Input File Button
    clickLocation = getClickLocation(win, 'input')
    
    #Sets input file and styles Input File Button after clicked
    infileName = inputSelection()
    inputButton.setStyle('italic')
    inputButton.setTextColor('light gray')
    #UnDraw Input File Selection
    inputButton.undraw()
    #Draws Output File button - Next step
    outputButton = Text(Point(200,70), "Select Output File").draw(win)

    #User Instruction
    print('\nClick "Select Output File" and navigate to where you would like the output saved and enter or keep default name for the new file, then Save.')
    #Get X/Y of mouse click and check if within Input File Button
    clickLocation = getClickLocation(win, 'input')
    #Sets output file and styles Output File Button after clicked
    outfileName = outputSelection()
    outputButton.setStyle('italic')
    outputButton.setTextColor('light gray')
    #UnDraw Output File Selection
    outputButton.undraw()
    #Draws Process Data button - Next step
    processButton = Text(Point(200,70), "Process QA Data").draw(win)

    #UserInstruction
    print('\nClick "Process QA Data" to produce the QA summary and the corresponding output file.')
    #Get X/Y of mouse click and check if within Input File Button
    clickLocation = getClickLocation(win, 'input')
    #Styles process data button after clicked
    processButton.setStyle('italic')
    processButton.setTextColor('light gray')
    #Assigns output dataframe to output variable
    output = processData(infileName, outfileName)


    #Initializes a spike, duplicate, and RPD instances of FailedSummary class
    spikeFailSummary = FailedSummary(output, 'SpikePassFail')
    duplicateFailSummary = FailedSummary(output, 'DuplicatePassFail')
    rpdFailSummary = FailedSummary(output, 'RPDPassFail')
    #Flowing Input Steps undraws the input file, output file, and process data buttons
    inputButton.undraw()
    outputButton.undraw()
    processButton.undraw()
    Rect.undraw()

    #Draws Open File button
    openButton = Text(Point(200,70), "Open Output File").draw(win)
    openRect = Rectangle(Point(120,50), Point(280,90)).draw(win)
    #Draws Exit button
    exitButton = Text(Point(200,150), "Exit").draw(win)
    exitRect = Rectangle(Point(120,130), Point(280,170)).draw(win)
    
    #Draws QA Summary Box
    summaryBox = Rectangle(Point(20,270), Point(380, 430)).draw(win)
    summaryMessage = Text(Point(80, 290), "QA Summary").draw(win)
    summaryMessage.setStyle('bold')
    #Spike QA Items - Number of Failed Items and Percent of Passing Items
    spikeFailCount = Text(Point(115, 310), "Spike Fail Count: " + str(spikeFailSummary.getFailedItems())).draw(win)
    spikePassPercent = Text(Point(125, 330), 'Pass Percentage: ' + str(100 - spikeFailSummary.getPercentFailed())).draw(win)
    spikePassPercent.setSize(10)
    #Duplicate QA Items - Number of Failed Items and Percent of Passing Items
    dupFailCount = Text(Point(128, 350), "Duplicate Fail Count: " + str(duplicateFailSummary.getFailedItems())).draw(win)
    dupPassPercent = Text(Point(125, 370), 'Pass Percentage: ' + str(100 - duplicateFailSummary.getPercentFailed())).draw(win)
    dupPassPercent.setSize(10)
    #Relative Percent Difference (Spike/Duplicate) - Number of Failed Items and Percent of Passing Items
    RPDFailCount = Text(Point(113, 390), "RPD Fail Count: " + str(rpdFailSummary.getFailedItems())).draw(win)
    RPDPassPercent = Text(Point(125, 410), 'Pass Percentage: ' + str(100 - rpdFailSummary.getPercentFailed())).draw(win)
    RPDPassPercent.setSize(10)

    print('\nReview the QA Summary section. For more detailed information select the Open Output File or select Exit')
    #Gets click location of output options (Exit or Open File)
    clickLocation = getClickLocation(win, 'output')
    #Opens output file or closes window when exit button clicked
    while clickLocation != 'exit':
        if clickLocation == 'open':
            startfile(outfileName)
            clickLocation = getClickLocation(win, 'output')
    #Mouse click location within Exit - Close main window
    win.close()
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def getClickLocation(w, input_output):
    """Check if the user has clicked within one of the action buttons on the interface window.
    Requires the graphics window and whether the program is at the input or output stage. Returns
    the name of the button clicked."""
    clickPoint = w.getMouse()
    button = buttonClick(clickPoint.getX(), clickPoint.getY(), input_output)

    while not button:
        clickPoint = w.getMouse()
        button = buttonClick(clickPoint.getX(), clickPoint.getY(), input_output)

    return button 
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def buttonClick(x, y, input_output):
    """Check the X Y position of user mouse click. Requires mouse click X and Y and whether input or 
    output button are visible and returns the name of the button clicked."""
    if input_output == 'input':
        if x >= 120 and x <= 280 and y >= 50 and y <= 90:
            return "input"
    elif input_output == 'output':
        if x >= 120 and x <= 280 and y >= 50 and y <= 90:
            return "open"
        elif x >= 120 and x <= 280 and y >= 130 and y <= 170:
            return "exit"
    
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def inputSelection():
    """Prompts the user to select the input file and verifies that a file was selected."""
    infileName = askopenfilename(title='Select the Input File', 
                                filetypes=(('CVS Files', '*.csv'),))
    #Verify a File was Selected
    verifyFileSelection(infileName)
    
    return infileName
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def outputSelection():
    """Prompts user to create or select output file and verifies that a file was selected."""
    #Selection of Requeired Output File
    outfileName = asksaveasfilename(title='Create Output File', 
                                        filetypes=(('CSV Files', '*.csv'),),
                                        defaultextension='.csv',
                                        initialfile='DefaultOutputFileName')
    #Verify Output File Selected
    verifyFileSelection(outfileName)

    return outfileName
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def verifyFileSelection (fileName):
    """Check that a file has been selected or if fileName is blank (i.e. "Cancel" selected)
    quit the program."""
    if fileName == '': 
        print('User Canceled.')
        quit()
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def processData(infileName, outfileName):
    """Function that requires the input and output file paths and calls a series of data processing
    functions, generates the output file and returns a dataframe of output data"""

    #Create Workable Input Data
    rawData = processInput(infileName)
    #Calculate OutPut Data    
    output = generateOutData(rawData)
    #Create Output CSV
    output.to_csv(outfileName, index=False)

    return output
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def processInput(infileName):
    """Creates a dataframe from the input CSV, and splits the Spike and Duplicate strings creating
    a list of values. Returns the rawData dataframe."""

    #Reads infile CSV and creates a DataFrame
    rawData = pandas.read_csv(infileName)
    #Splits the Input Spike/Duplicate columns by ';' and returns column as a list
    rawData['Spike'] = rawData['Spike'].str.split(';')
    rawData['Duplicate'] = rawData['Duplicate'].str.split(';')
    
    return rawData
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def generateOutData(input):
    """Iterates through raw data creating a QA class instance for each row in the dataframe. Appends
    QA metrics and pass/fail determination to outData data."""

    #Empty Dataframe to be populated for each QA Item
    outData = pandas.DataFrame(columns=(['ID', 'SpikeRecovery', 'SpikePassFail', 'DuplicateRecovery', 'DuplicatePassFail', 'RPD', 'RPDPassFail']))
    
    #Loop through input and pass each row to the QA Class creating a instance with QA calculations
    for index, row in input.iterrows():
        qaID = row['ID']
        qaID = QA(row)
        ##Appends each items QA data to the outData dataframe
        outData = outData.append({'ID':row['ID'],
                                    'SpikeRecovery': qaID.getSpikeRecovery(),
                                    'SpikePassFail':qaID.getSpikePassFail(),
                                    'DuplicateRecovery':qaID.getDupRecovery(),
                                    'DuplicatePassFail':qaID.getDupPassFail(),
                                    'RPD': qaID.getRPD(),
                                    'RPDPassFail': qaID.getRPDPassFail()}, 
                                    ignore_index=True)
    return outData
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
class QA:
    """Initailzes a QA object extracting required information from Spike/Duplicate string from the input
    data and calculates the percent recovery, determines if each item passed or failed relative to limits, 
    and calculates the relative percent difference between the spike and duplicate items."""
    def __init__(self, rowData):
        self.Data = rowData
        
        self.Spike = float(self.Data[2][4])
        self.spikeConc = self.Concentration(self.Data[2][1], self.Data[2][2], self.Data[2][3])
        self.spikeRecovery = self.Recovery(self.Data[1], self.Spike, self.spikeConc)
        self.spikePassFail = self.PassFail(self.spikeRecovery)

        self.Duplicate = float(self.Data[3][4])
        self.dupConc = self.Concentration(self.Data[3][1], self.Data[3][2], self.Data[3][3])
        self.dupRecovery = self.Recovery(self.Data[1], self.Duplicate, self.dupConc)
        self.dupPassFail = self.PassFail(self.dupRecovery)

        self.RPD = round(abs(self.Spike - self.Duplicate) / ((self.Spike + self.Duplicate) / 2) * 100,2)
        self.RPDPassFail = self.PassFail(self.RPD, rpd=True)

    def Concentration(self, concentrate, aliquot, volume):
        """Calculates and returns the expected concentration utlizing input file values"""
        Conc = float(concentrate) * float(aliquot) / float(volume)
        return Conc
    def Recovery(self, original, spike, concentration):
        """Calculates and returns the percent reovery of the spike/duplicate QA items"""
        Recovery = round(abs((float(original) - float(spike))) / concentration * 100, 2)
        return Recovery
    def PassFail(self, qaMeasure, rpd = False):
        """Compares the Reovery values or RPD to respective limits and returns Pass or Fail"""
        if rpd == False:
            if float(qaMeasure) < 90 or qaMeasure > 110:
                return "Fail"
            else:
                return "Pass"
        else:
            if float(qaMeasure) > 20:
                return "Fail"
            else:
                return "Pass"
    
    def getOriginal(self):
        """Return the Original value for the QA Item"""
        return self.Data[1]
    def getSpike(self):
        """Return the Spike value for the QA Item"""
        return self.Spike
    def getDuplicate(self):
        """Return the Duplicate value for the QA Item"""
        return self.Duplicate
    def getSpikeRecovery(self):
        """Return the Percent Recovery of the Spike QA Item"""
        return self.spikeRecovery
    def getDupRecovery(self):
        """Return the Percent Recovery of the Duplicate QA Item"""
        return self.dupRecovery
    def getSpikePassFail(self):
        """Return Pass or Fail for the Spike QA Item"""
        return self.spikePassFail
    def getDupPassFail(self):
        """Return the Pass or Fail for the Duplicate QA Item"""
        return self.dupPassFail
    def getRPD(self):
        """Return the Relative Percent Difference of the Spike and Duplicate QA Items"""
        return self.RPD
    def getRPDPassFail(self):
        """Return the Pass or Fail for the RPD"""
        return self.RPDPassFail
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
class FailedSummary:
    """Initializes FailedSummary and calculates the total number of QA items, the number of items that
    have a PassFail equal to Fail, and the percent of failed items."""
    def __init__(self, data, measure):
    
        self.totalItems = len(data.index)
        self.failedItems = len(data[data[measure]=='Fail'])
        self.percentFailed = round(self.failedItems / self.totalItems * 100, 2)

    def getTotalItems(self):
        return self.totalItems
    def getFailedItems(self):
        return self.failedItems
    def getPercentFailed(self):
        return self.percentFailed
#-------------------------------------------------------------------------------------------------
