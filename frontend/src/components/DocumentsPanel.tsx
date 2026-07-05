import type { DocumentItem } from '../services/api';
import { getStorageUrl } from '../services/api';

interface Props {
  documents: DocumentItem[];
  loading: boolean;
}

function formatTime(ts: string | null): string {
  if (!ts) return '';
  return new Date(ts).toLocaleString();
}

export default function DocumentsPanel({ documents, loading }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Documents</h3>
      {loading ? (
        <p className="text-sm text-gray-400">Loading...</p>
      ) : documents.length === 0 ? (
        <p className="text-sm text-gray-400">No documents yet. Send a document via WhatsApp.</p>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 border-b border-gray-100 pb-2 last:border-0"
            >
              <a
                href={getStorageUrl(doc.file_path)}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:underline break-all"
              >
                {doc.filename}
              </a>
              <span className="text-xs text-gray-400 sm:ml-2 shrink-0">{formatTime(doc.created_at)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
