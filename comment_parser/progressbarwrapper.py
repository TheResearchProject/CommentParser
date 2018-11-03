from progressbar import ProgressBar, \
    SimpleProgress, Percentage, Bar, Timer, AdaptiveETA

class ProgressBarWrapper():
    def __init__(self, maxval, alternate = False):
        self.done = 0
        if alternate:
            pbar_widgets = [FormatLabel('Processed: %(value)d/%(max)d items (in: %(elapsed)s)'), 
               ' -=- ', Percentage(),
               ' -=- ', ETA()]  
            self.pbar = ProgressBar(widgets=pbar_widgets, 
                                    maxval=maxval, 
                                    endline_character="\n")           
        else:
            pbar_widgets = [SimpleProgress(),
               ' ', Percentage(),
               ' ', Bar(),
               ' ', Timer(),
               ' ', AdaptiveETA()]   
            self.pbar = ProgressBar(widgets=pbar_widgets, 
                                maxval=maxval)
        if alternate:
            self.pbar.update_interval = maxval/50
        self.pbar.start()         
        
    def increment(self, x=1):
        self.done += x
        self.pbar.update(self.done)  
        
    def destroy(self):
        self.pbar.finish()