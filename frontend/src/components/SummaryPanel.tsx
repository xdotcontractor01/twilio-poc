interface Props {
  notesCount: number;
  imagesCount: number;
  documentsCount: number;
}

export default function SummaryPanel({ notesCount, imagesCount, documentsCount }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Activity Summary</h3>
      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <p className="text-2xl font-semibold text-gray-900">{notesCount}</p>
          <p className="text-xs text-gray-500 mt-1">Notes</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-semibold text-gray-900">{imagesCount}</p>
          <p className="text-xs text-gray-500 mt-1">Images</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-semibold text-gray-900">{documentsCount}</p>
          <p className="text-xs text-gray-500 mt-1">Documents</p>
        </div>
      </div>
    </div>
  );
}
