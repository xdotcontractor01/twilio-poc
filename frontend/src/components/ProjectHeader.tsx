import type { Project } from '../services/api';

interface Props {
  project: Project;
}

export default function ProjectHeader({ project }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 md:p-6">
      <h2 className="text-lg md:text-xl font-semibold text-gray-900 break-words">{project.name}</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        <div>
          <span className="text-xs text-gray-500 uppercase">Code</span>
          <p className="text-sm font-mono text-gray-900">{project.code}</p>
        </div>
        <div>
          <span className="text-xs text-gray-500 uppercase">Project Manager</span>
          <p className="text-sm text-gray-900 break-words">{project.manager}</p>
        </div>
        <div>
          <span className="text-xs text-gray-500 uppercase">Contractor</span>
          <p className="text-sm text-gray-900 break-words">{project.contractor}</p>
        </div>
        <div>
          <span className="text-xs text-gray-500 uppercase">Status</span>
          <p className="text-sm text-gray-900">{project.status}</p>
        </div>
        <div className="sm:col-span-2 lg:col-span-1">
          <span className="text-xs text-gray-500 uppercase">Completion</span>
          <div className="flex items-center gap-2 mt-0.5">
            <div className="flex-1 min-w-0 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded-full"
                style={{ width: `${project.completion_percentage}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 shrink-0">
              {project.completion_percentage}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
