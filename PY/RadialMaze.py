# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 22:43:59 2025

@author: Violet
"""

# Import Libraries
import os
import time
import matplotlib.pyplot as plt
from collections import deque
from Modules.GLComponents import ssi, FileDrivenMaze, wells, well_callback
try:
    from Modules.RadialMazeDataProcessing import Epoch, Block, Trial, Poke
except:
    from RadialMazeDataProcessing import Epoch, Block, Trial, Poke

"""
Enums
"""

class groups:
    """A Pseudo-Enum Containing the Reward Well Group Names"""
    home = 'home'
    arms = 'arms'

class phases:
    """An Enum Containing the Maze Phase Codes"""
    start = -2
    lockend = -1
    home = 0
    arms = 1
    lockout = 2
    end = 3


"""
Open the Log
"""

# the rat you're currently working with
name = 'demo'

# whether or not to enable live plotting of the data
live_plot = True

# path constants
slash = ssi.filepath_separator

# check if the environemnt is my dev environment
if slash == '\\': # equivalent to checking if the environment is Windows (my computer) or Linux (the machines downstairs)
    debug = True
    # override the paths for the parameter file and the log file
    #filepath = r"C:\Users\Violet\Downloads\template_parameter-log.txt"
    filepath = r"C:\Users\Violet\Downloads\demo_parameter-log.txt"
    ssi.open_log(name, r"C:\Users\Violet\Downloads")
else:
    # derived path values for the parameter file and the log file
    debug = False
    name = name.lower()
    desktop = slash.join(os.getcwd().split(slash)[:-2])
    root = f"{desktop}{slash}6-Arm-Training-Plans"
    filepath = f"{root}{slash}{name}_parameter-log.txt"
    
    # open a new log file
    ssi.open_log(name, f"{desktop}{slash}6-Arm_BC_Logs")

tablepath = ssi.logger.filepath[:-4] + '.rmTableData'

"""
Set the Config
"""

# set the config
ssi.functions = {
    'stats': 1,             #  print the stats
    'reset': 4,             #  reset all StateScript variables, and re-prime the pumps
    'lockout': 5,           #  begin a lockout
    'end epoch': 6,         #  end the epoch
    'small reward': 10,     #  deliver a small reward
    'medium reward': 11,    #  deliver a medium reward
    'large reward': 12      #  deliver a large reward
}
well_mapping = [7,1,2,3,4,5,6]  #  ports assigned to each well (home, arms 1-n)
pump_mapping = [15,9,10,11,12,13,14]  #  ports assigned to each pump (home, arms 1-n)
wells.configure(well_mapping, pump_mapping, 
    {
        groups.home: ((1, 'small reward'), 1),
        groups.arms: ((0, 'large reward'), 6)
    }
)

# Reset the StateScript Variables and Re-Prime the Pumps
ssi.trigger('reset')

# No 2 Wells Should be Triggered at Once
wells.forbid_simultaneous_pokes()


"""MAZE OBJECTS"""

# an object which manages the displayed statistics (Anna, I'd recommend you just copy this/edit the data)
class Stats:
    # the names of the stats variables in StateScript (keys are the names of the equivalent variables in python)
    var_names = {
        'home': 'homeCount',
        'goals': 'goalTotal',
        'other': 'otherCount',
        'this_goal': 'goalCount',
        'lock': 'lockCount'
    }
    
    def __init__(self, arms:int):
        """an object for tracking/updating the stats we print in StateScript"""
        
        # Initialize the Paired Attributes while By-Passing the __setattr__ Method
        # this means that when we set those variables to 0 it will also reset them in StateScript
        for name in Stats.var_names: self.__dict__[name] = None
        
        # Initialize the Parameters, and Set the Paired StateScript Variables
        self.home = 0
        self.goals = 0
        self.goal_counts = [0]*(arms + 1)
        self.this_goal = 0
        self.other = 0
        self.lock = 0
        self.blocks = 0
    
    # this runs every time an attribute is set (and makes sure the stats in statescript mirrors the stats in python)
    def __setattr__(self, name:str, value:int):
        # check if there's a statescript variable to update
        if name in Stats.var_names and self.__dict__[name] != value:
            # update the variable in statescript
            ssi.set_var(Stats.var_names[name], value)
        
        # update the value of the variable
        self.__dict__[name] = value
    
    def __str__(self):
        attributes = ['home', 'lock', 'goals', 'other', 'goal_counts']
        return '\n'.join(map(lambda key: f"{key}: {self.__dict__[key]}", attributes))

class PreProcessor(Epoch):
    def __init__(self, filepath:str, maze, plot:bool = True):
        self.index = None
        self.date, self.name, self.epoch_number = Epoch._filename_parsers['log'](ssi.logger.filename)
        self.filepath = filepath
        self.maze = maze
        self.parameters = maze # this is really the RadialMaze object, which extends the ParameterFile object
        self.plot = plot
        self.blocks = []
        self.trials = []
        
        Trial.trial_num = 0
        Trial.current = Trial(None)
        
        self.unplotted_pokes = deque()
        
        self.complete = False
        
        self.active = True
        
        self.x = 1
        outreps = sum(self.parameters.outreps)/len(self.parameters.outreps) if hasattr(self.parameters.outreps, '__iter__') else self.parameters.outreps
        self.X = self.parameters.max_trials + 2 if self.parameters.max_trials > -1 else int(self.parameters.goal_blocks * outreps / self.parameters.success_threshold)
        self.fig = None
        self.ax = None
        
        self.open_file()
        self.init_plot()
    
    def open_file(self):
        data = self.to_table_entry(include_index = False)
        line = Epoch.rmParamsParser.build(data)
        with open(self.filepath, 'w') as file:
            file.write(line)
            file.write('\n')
            file.close()
    
    def log_current_trial(self):
        if self.active and Trial.current and Trial.current.trial_num:
            # Replace Null Data with a Sentinel
            null_values = []
            for name, value in Trial.current.__dict__.items():
                if value == None:
                    null_values.append(name)
                    value = -1
                    if name == 'outer':
                        value = Poke(-1, False, self.maze.phase, self.maze.search_mode, Block.current.goal, -1, -1, Trial.current)
                    Trial.current.__dict__[name] = value
                    
            # Make Sure the Goal is Present/Formatted
            goal = Trial.current.block.goal
            if not Trial.current.block.goal:
                Trial.current.block.goal = [w.index for w in self.maze.goal]
            
            # Get the Data, and Create the String
            data = Trial.current.to_table_entry(include_index = False)
            line = Epoch.rmTrialParser.build(data)
            
            # Add the Line to the File
            with open(self.filepath, 'a') as file:
                file.write(line)
                file.write('\n')
                file.close()
            
            # Fix the Edits to the Data
            Trial.current.block.goal = goal
            for name in null_values:
                Trial.current.__dict__[name] = None
    
    def _try_plot(self, method, *args):
        """a wrapper to make sure plotting never breaks anything"""
        try:
            if self.plot and self.active:
                method(*args)
        except:
            print('warning: unable to initialize the live plot; live plot disabled')
            self.plot = False
    
    def _init_plot(self):
        
        def on_close(event):
            self.plot = False
        
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('close_event', on_close)
        plt.suptitle(ssi.logger.filename[:-4].replace('_', ' ') + ": Running")
        plt.ylabel('Arm Number')
        plt.xlabel('Trials + Lockouts')
        self._set_axis_params()
        plt.show()
    
    def _set_axis_params(self):
        plt.ylim(0.8, 6.2)
        self.fig.set_figheight(5)
        self._set_xaxis_lims()
        plt.ylabel('Arm Number')
        plt.xlabel('Trials + Lockouts')
    
    def _set_xaxis_lims(self):
        try:
            if self.plot and self.active:
                plt.xlim(0, self.X)
                self.fig.set_figwidth(self.X / 6)
        except:
            pass
    
    def _update_plot_full(self):
        self.ax.cla()
        self._set_axis_params()
        self.x = self.raster_plot(axes = self.ax, included = 1, black_line = False)
        if self.x > self.X:
            self.X = self.x
            self._set_axis_params()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def _update_plot(self):
        while self.unplotted_pokes:
            poke = self.unplotted_pokes.popleft()
            marker = '.' if poke.rewarded else '+'
            color = 'grey' if hasattr(poke, 'lockout') and poke.lockout else 'magenta'
            plt.errorbar(self.x, 0 if poke.is_home else poke.well, fmt = marker, color = color)
            self.x += 1
        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()
    
    def _add_block_divider(self):
        self.update_plot() # this is necessary to make sure self.x is accurate
        if self.maze.outreps != 1 and self.x > 1:
            self.ax.plot([self.x - 0.5]*2, [0, 8], color = 'lightgrey')
    
    def init_plot(self):
        self._try_plot(self._init_plot)
    
    def add_block_divider(self):
        self._try_plot(self._add_block_divider)
    
    def update_plot(self):
        self._try_plot(self._update_plot)
    
    def new_block(self, t:int) -> None:
        # Clean Up the Current Block
        if Block.current: 
            self.add_block_divider()
        
        # Start a New Block
        Block.current = Block(self)
        Block.current.goal = [w.index for w in self.maze.goal]
        self.outreps = self.maze.reps_remaining
        Block.current.all_trials = Block.current.trials
        Block.current.start = t
        self.blocks.append(Block.current)
    
    def new_trial(self, t:int) -> None:
        # Cleanup the Previous Trial
        Trial.current._on_load()
        self.log_current_trial()
        self.update_plot()
        
        # Start a New Trial
        Trial.current = Trial(Block.current, Poke.current)
        Trial.current.reps_remaining = self.maze.reps_remaining
        self.first_trial = False
        
        # Add the Trial to the Trial Lists
        Block.current.trials.append(Trial.current)
        self.trials.append(Trial.current)
    
    def _poke(self, t:int, well, rewarded:bool) -> Poke:
        return Poke(well.index, rewarded, self.maze.search_mode, self.maze.phase, self.maze.goal, t, None)
    
    def add_home(self, t:int, well) -> None:
        # Start a New Trial
        self.new_trial(t)
        
        # Make a New Poke Object
        self._poke(t, well, True)
        Poke.current.is_home = True
        #self.unplotted_pokes.append(Poke.current)
        
        # Add the Poke to the Trial
        Trial.current.add_home()
    
    def add_outer(self, t:int, well, rewarded:bool) -> None:
        # Make a New Poke Object
        self._poke(t, well, rewarded)
        Poke.current.is_home = False
        
        # Add the Poke to the Trial
        Trial.current.add_outer()
        Trial.current.complete = True # includes the trial in the plot
        
        # Update the Plot
        self.unplotted_pokes.append(Poke.current)
        self.update_plot()
        
        # Fix the Search Mode Bug
        if Trial.current.index == 0 and len(self.blocks) > 1:
            try: Trial.current._on_load()
            except: pass
    
    def add_lockout(self, t:int, well) -> None:
        # Make a New Poke Object
        self._poke(t, well, False)
        Poke.current.is_home = False
        Poke.current.lockout = True
        self.unplotted_pokes.append(Poke.current)
        self.update_plot()
        
        # Add the Poke to the Current Trial's Lockout List
        Trial.current.add_lockout()
        
        # Update the Plot
        self.X += 1
        self._set_xaxis_lims()
    
    def down(self, t):
        Trial.current.end = t
        if Poke.current:
            Poke.current.end = t
        
    def close(self, t):
        if Trial.current: 
            Trial.current._on_load()
            if Trial.current.end == None != t:
                Trial.current.end = t
        if Block.current:
            Block.current._on_load()
        self.log_current_trial()
        self.update_plot()
        if self.plot and self.active:
            plt.suptitle(ssi.logger.filename[:-4].replace('_', ' ') + ": Complete")
        self.active = False
        if not self.plot:
            self.raster_plot()

class RadialMaze(FileDrivenMaze):
    def __init__(self, filepath):
        # Load the Maze Parameters From the File
        super(RadialMaze, self).__init__(filepath)
        
        # Get the Wells by Group for Ease of Access
        self.home = wells[groups.home][0]
        self.outer_wells = wells.groups[groups.arms]
        
        # Log the Parameter File
        self.log_parameter_file('PARAMETER FILE (INITIAL):')
        ssi.logger.add_line_break()
        
        # Initialize Other Parameters
        self.arms = self.possible_goal_count
        self.phase = phases.start
        self.successful_epoch = False
        self.timeout_grace_period = 10
        self.end_epoch_next_home = False
        self.reward_error = False
        
        # Initialize the Stats Objects
        self.stats = Stats(self.arms)
        self.pokes = [[]]
        self.search_mode = 1 # used when recording the pokes
        
        # Set the StateScript Parameters
        ssi.set_var('lockoutPeriod', 1000 * self.delay)
        
        # Print the Maze Parameters
        self.print_params()
        
        # Initialize the Pre-Processor
        self.pre_processor = PreProcessor(tablepath, self, live_plot)
    
    def log_parameter_file(self, header:str = None):
        """Save a Copy of the Parameter File in the Log"""
        ssi.logger.add_line_break()
        if header != None: ssi.logger.add_line_without_timestamp(header)
        for line in self.get_parameter_file_lines(): ssi.logger.add_line_without_timestamp(line)
    
    # Override the Goal Selection
    def select_goal(self, t:int):
        """Select the Next Goal (Begins a New Goal Block)"""
        super(RadialMaze, self).select_goal(self.outer_wells)
        self.pre_processor.new_block(t)
    
    # On Maze Ready
    def ready(self, t):
        """Do things which should only happen after the pumps have finished re-priming"""
        # Start the Epoch Timer in StateScript
        self.home.activate(True)
        self.start_time = time.time()
        wells.forbid_simultaneous_rewards()
        ssi.disp(f'maze initialization completed at {ssi.get_timestamp()} [backup epoch timer started]')
        ssi.logger.add_line_break()
        Trial.current.start = t
        self.select_goal(t)
    
    def up(self, t, well):
        # Record the Poke
        rewarded = well.reward_given
        poke = (well.index, int(rewarded), int(self.search_mode), self.phase, [w.index for w in self.goal], t)
        self.pokes[-1].append(poke)
        ssi.log(f"poke: {poke}")
        
        # Check for Lockout
        if maze.phase == phases.lockout:
            self.pre_processor.add_lockout(t, well)
            return
        
        if well != self.home and self.search_mode and rewarded:
            self.search_mode = 0
        
        # Record the Actual Start Time
        if len(self.pokes) == 1 and len(self.pokes[-1]) == 1 and time.time() + self.timeout - self.timeout_grace_period < self.start_time + self.timeout:
            self.start_time = time.time()
            self.timeout_grace_period = 0 # remove the grace period
            ssi.disp(f'epoch timer started at {ssi.get_timestamp()}')
        
        # Check Where the Poke Happened
        if well == self.home:
            if rewarded:
                # Start a New Trial in the Data
                self.pre_processor.add_home(t, well)
                
                # Update the Home Count
                self.stats.home += 1
                
                # Activate the Goal/LEDs
                self.home.deactivate()
                wells.activate(self.goal)
                wells.set_leds(self.leds, 1)
                
                # Update the Phase
                self.phase = phases.arms
            else:
                # Add the Home Poke as a Lockout in the Data
                self.pre_processor.add_lockout(t, well)
        else:
            # Record the Poke
            self.total_visits[well.index - 1] += 1
            self.updated_weighted_visits(well.index, rewarded)
            
            if rewarded:
                # Add the Outer Poke to the Data
                self.pre_processor.add_outer(t, well, rewarded)
                
                # Update the Stats
                self.rewarded_visits[well.index - 1] += 1
                self.stats.goal_counts[well.index - 1] += 1
                self.stats.goals += 1
                self.stats.this_goal += 1
                self.reps_remaining -= 1
                ssi.disp(f"reps remaining: {self.reps_remaining}")
                
                # Update the Goal
                if self.forageassist:
                    self.goal = [well]
                
                # Update the Phase
                self.phase = phases.home
            elif self.phase == phases.arms:
                # Add the Outer Poke to the Data
                self.pre_processor.add_outer(t, well, rewarded)
                
                # Update the Stats
                self.stats.other += 1
                
                # Update the Phase
                self.phase = phases.home
            elif self.phase <= phases.home: # relies on 2 up pokes not happening in a row
                # Add the Lockout Poke to the Data
                self.pre_processor.add_lockout(t, well)
                
                # Begin a Lockout
                if self.phase == phases.home:
                    self.lockout()
            
            # Update the Well Activation
            if self.phase != phases.lockout:
                wells.deactivate(groups.arms)
                self.home.activate()
    
    def down(self, t, well):
        """On a DOWN Poke, Either Update the LEDs or End the Epoch"""
        # Record the Down Poke
        self.pre_processor.down(t)
        
        # check if the epoch is over
        if (self.end_mode == 0 and self.stats.home > self.max_trials) or (well == self.home and self.end_epoch_next_home) or self.timed_out():
            # End the Epoch
            self.end_epoch()
        else:
            # set the LEDs
            wells.update()
            
            # choose a new goal
            if not self.reps_remaining:
                ssi.disp('goal block complete')
                ssi.logger.add_line_break(char = '-')
                self.search_mode = 1
                self.stats.blocks += 1
                if self.end_mode == 1 and self.stats.blocks >= self.goal_blocks:
                    # Set the Epoch to End
                    self.end_epoch_next_home = True
                else:
                    self.select_goal(t)
                    self.stats.this_goal = 0
                    self.pokes.append([])
    
    def lockout(self, t = None):
        """Begin a Lockout Period"""
        # Begin the Lockout
        self.phase = phases.lockout
        ssi.trigger('lockout')
        
        # Turn Off All Wells
        #wells.deactivate()
        self.home.deactivate()
        
        # Update the Lock Count
        self.stats.lock += 1
    
    def lockend(self, t = None):
        """End a Lockout Period"""
        # Turn the Home Well On
        self.phase = phases.lockend
        self.home.activate(True)
    
    def end_epoch(self, t = None):
        """Full Procedure to End the Epoch"""
        # Set the Maze Phase
        self.phase = phases.end
        
        # Turn Off All the Wells
        wells.deactivate(update = True)
        
        # Log the Parameter File (after edits)
        if self.filepath:
            self.log_parameter_file('PARAMETER FILE (FINAL):')
        
        # Close the Log
        ssi.close_log()
        
        # Close the Pre-Processor
        self.pre_processor.close(t)
    
    def check_success_rate(self):
        if not self.max_epochs_updated and self.stats.home > 1: # must have 1 trial to decrement the epoch counter
            self.max_epochs_remaining -= 1
            self.max_epochs_updated = True
        
        success = False
        if self.stats.goals|self.stats.other and [self.stats.home > self.min_trials, self.stats.blocks][self.end_mode]:
            if type(self.success_threshold) == int:
                if self.success_threshold < 10:
                    success = self.stats.blocks >= self.success_threshold
                    ssi.disp(f'blocks completed: {self.stats.blocks}, target: {self.success_threshold}')
                else:
                    success = self.stats.goals >= self.success_threshold
                    ssi.disp(f'goals found: {self.stats.goals}, target: {self.success_threshold}')
            else:
                r = self.stats.goals / (self.stats.goals + self.stats.other)
                success = r >= self.success_threshold
                ssi.disp(f'success rate: {round(100*r, 1)} [threshold: {round(100*self.success_threshold, 1)}]')
        
        if [self.stats.home > self.min_trials, self.stats.blocks >= maze.goal_blocks][self.end_mode]:
            ssi.disp('epoch complete: all trials finished')
        elif self.timed_out():
            ssi.disp('epoch complete: timed out')
        
        if success != self.successful_epoch:
            self.successful_epoch = success
            if success:
                self.successful_epochs_remaining -= 1
            else:
                self.successful_epochs_remaining += 1
        
        return self.successful_epoch

# Load the Maze
maze = RadialMaze(filepath)
ssi.config.add_commands({
    'UP': maze.up,              #  triggered the first time a rat puts its nose in a well
    'DOWN': maze.down,          #  triggered when a rat pulls its nose out of a well
    'LOCKEND': maze.lockend,    #  indicates the end of a lockout
    'READY': maze.ready,        #  indicates that the maze has finished resetting variables and re-priming the pumps
    'STOP': maze.end_epoch,     #  command to end the epoch
})

@ssi.command('REWARD_ERROR')
def set_reward_error(t:int = None) -> None: maze.reward_error = True #  triggered when the maze attempts to deliver multiple rewards simultaneously

@ssi.command('PING')
def ping(t:int = None) -> None:
    if maze.timed_out():
        maze.end_epoch()

# Define the Callback Function
def callback(line):
    # Process the Command (based on the maze's current state and the contents of the command)
    if maze.phase < phases.end and well_callback(line):
        if maze.reward_error: 
            ssi.disp('CHECK REWARD WELLS')
        maze.check_success_rate()
        maze.save_to_file()
        if maze.timed_out():
            maze.end_epoch()
    elif maze.phase == phases.end and ssi.command_is_valid(line):
        ssi.print_stats()
        if maze.reward_error: 
            ssi.disp('CHECK REWARD WELLS')
        maze.check_success_rate()

# Helper Object for Testing
if debug:
    class Poker:
        def __init__(self, home = 7, downs:int = 3):
            self.home = home
            self.downs = downs
            self.t = 0
            self._callback('READY')
        
        def _callback(self, command:str):
            callback(f"{self.t} {command}")
            self.t += 1
        
        def poke(self, well:int):
            self._callback(f"UP {well}")
            for _ in range(self.downs): 
                self._callback(f"DOWN {well}")
        
        def trial(self, well:int):
            self.poke(self.home)
            self.poke(well)
        
        def __call__(self, well:int, pokes:int = 1, full_trial:bool = True):
            if full_trial:
                for _ in range(pokes): self.trial(well)
            else:
                for _ in range(pokes): self.poke(well)
        
        def lockend(self):
            self._callback("LOCKEND")
    
    poke = Poker()
