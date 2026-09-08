export type SessionStatus = "queued" | "running" | "completed" | "cancelled";

export interface Session { id: string; status: SessionStatus; workerId?: string }

export function reconcile(session: Session, workerAlive: boolean): Session {
  if (session.status === "running" && !workerAlive) return { ...session, status: "cancelled" };
  return session;
}

export const fixture: Session = { id: "s-42", status: "running", workerId: "missing-worker" };
