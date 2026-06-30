'use client';

import { KanbanColumn } from './KanbanColumn';
import { KanbanBoard, Application } from '@/hooks/api/workflow';

interface ApplicationBoardProps {
  kanbanBoard: KanbanBoard;
  onApplicationClick?: (application: Application) => void;
  onApplicationEdit?: (application: Application) => void;
  onApplicationDelete?: (application: Application) => void;
}

export function ApplicationBoard({
  kanbanBoard,
  onApplicationClick,
  onApplicationEdit,
  onApplicationDelete,
}: ApplicationBoardProps) {
  return (
    <div className="flex space-x-4 overflow-x-auto pb-4">
      {kanbanBoard.columns.map((column) => (
        <KanbanColumn
          key={column.id}
          id={column.id}
          title={column.title}
          status={column.status}
          applications={column.applications}
          onApplicationClick={onApplicationClick}
          onApplicationEdit={onApplicationEdit}
          onApplicationDelete={onApplicationDelete}
        />
      ))}
    </div>
  );
}
