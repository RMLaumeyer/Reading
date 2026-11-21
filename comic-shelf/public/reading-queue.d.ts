export type Queue = Record<string, {status: string; updatedAt: number}>;
export const queueKey: string;
export const statuses: string[][];
export function readQueue(storage?: Storage): Queue;
export function saveStatus(id: string, status: string, storage?: Storage): Queue;
