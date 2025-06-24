import React from 'react';
import { UserProgress } from '../types';
import { CheckCircle, Calendar, RotateCcw } from 'lucide-react';

interface ProgressBarProps {
  progress: UserProgress;
  onNewMonth?: () => void;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ progress, onNewMonth }) => {
  const percentage = Math.min((progress.completedDays / progress.totalDays) * 100, 100);
  const isComplete = progress.completedDays >= progress.totalDays;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <CheckCircle className="h-5 w-5 text-green-500" />
          <span className="text-sm font-medium text-gray-700">
            {Math.min(progress.completedDays, progress.totalDays)} of {progress.totalDays} days completed
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-5 w-5 text-gray-400" />
            <span className="text-sm text-gray-500">
              Started: {new Date(progress.startDate).toLocaleDateString()}
            </span>
          </div>
          {isComplete && onNewMonth && (
            <button
              onClick={onNewMonth}
              className="flex items-center space-x-1 text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg transition-colors"
            >
              <RotateCcw className="h-4 w-4" />
              <span>New Month</span>
            </button>
          )}
        </div>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-300 ${
            isComplete 
              ? 'bg-gradient-to-r from-green-500 to-green-600' 
              : 'bg-gradient-to-r from-primary-500 to-primary-600'
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="text-center">
        <span className={`text-2xl font-bold ${isComplete ? 'text-green-600' : 'text-primary-600'}`}>
          {Math.round(percentage)}%
        </span>
        <p className="text-sm text-gray-600 mt-1">
          {isComplete 
            ? 'Congratulations! You\'ve completed your 20-day tracking period.' 
            : `${progress.totalDays - progress.completedDays} days remaining`
          }
        </p>
        {isComplete && (
          <p className="text-sm text-green-600 mt-2 font-medium">
            Ready for AI prediction analysis! Click "New Month" to start tracking a new period.
          </p>
        )}
      </div>
    </div>
  );
};

export default ProgressBar;