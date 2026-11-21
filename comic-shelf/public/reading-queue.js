export const queueKey = 'panel.reading-queue.v1';
export const statuses = [['none','Not in queue'],['want','Want to read'],['reading','Reading'],['finished','Finished']];
export function readQueue(storage = localStorage) {
 const raw = storage.getItem(queueKey); if (!raw) return {};
 const data = JSON.parse(raw);
 if (!data || typeof data !== 'object' || Array.isArray(data)) throw Error('Invalid queue');
 return Object.fromEntries(Object.entries(data).filter(([,v]) => v && ['want','reading','finished'].includes(v.status) && Number.isFinite(v.updatedAt)));
}
export function saveStatus(id, status, storage = localStorage) {
 if (!statuses.some(([key]) => key === status)) throw Error('Invalid status');
 const queue = readQueue(storage);
 if (status === 'none') delete queue[id]; else queue[id] = {status, updatedAt: Date.now()};
 storage.setItem(queueKey, JSON.stringify(queue)); return queue;
}
