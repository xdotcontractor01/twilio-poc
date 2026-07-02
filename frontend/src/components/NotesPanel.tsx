import type { NoteItem } from '../services/api';

interface Props {
  notes: NoteItem[];
  loading: boolean;
}

function formatTime(ts: string | null): string {
  if (!ts) return '';
  return new Date(ts).toLocaleString();
}

export default function NotesPanel({ notes, loading }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Notes</h3>
      {loading ? (
        <p className="text-sm text-gray-400">Loading...</p>
      ) : notes.length === 0 ? (
        <p className="text-sm text-gray-400">No notes yet. Send a text via WhatsApp.</p>
      ) : (
        <div className="space-y-3 max-h-64 overflow-y-auto">
          {notes.map((note) => (
            <div key={note.id} className="border-b border-gray-100 pb-2 last:border-0">
              <p className="text-sm text-gray-900">{note.message}</p>
              <div className="flex gap-3 mt-1">
                <span className="text-xs text-gray-500">{note.sender}</span>
                <span className="text-xs text-gray-400">{formatTime(note.created_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
