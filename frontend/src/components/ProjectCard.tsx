import type { Project } from '../services/api';

interface Props {
  project: Project;
  selected: boolean;
  onClick: () => void;
}

export default function ProjectCard({ project, selected, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className={`shrink-0 md:shrink w-[180px] md:w-full text-left p-3 rounded-lg border transition-colors cursor-pointer ${
        selected
          ? 'border-blue-500 bg-blue-50 shadow-sm'
          : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
      }`}
    >
      <div className="text-xs font-mono text-gray-500">{project.code}</div>
      <div className="text-sm font-medium text-gray-900 mt-0.5 line-clamp-2">{project.name}</div>
      <div className="text-xs text-gray-500 mt-1">{project.status}</div>
    </button>
  );
}
