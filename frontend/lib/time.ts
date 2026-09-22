export type DisplayZone = "UTC" | "UTC+1";
export function zonePreference(): DisplayZone {
  if (typeof window === "undefined") return "UTC+1";
  return (localStorage.getItem("headroom-time-zone") as DisplayZone) || "UTC+1";
}
export function saveZonePreference(zone: DisplayZone) { localStorage.setItem("headroom-time-zone", zone); }
export function toUnixSeconds(value: string, zone: DisplayZone = zonePreference()): number {
  if (!value) throw new Error("Choose a date and time.");
  const normalized = value.length === 16 ? `${value}:00` : value;
  const utcMillis = Date.parse(`${normalized}Z`) - (zone === "UTC+1" ? 60 * 60_000 : 0);
  if (!Number.isFinite(utcMillis)) throw new Error("Enter a valid date and time.");
  return Math.floor(utcMillis / 1000);
}
export function fromUnixSeconds(seconds: number, zone: DisplayZone = zonePreference()): string {
  const shifted = new Date(seconds * 1000 + (zone === "UTC+1" ? 60 * 60_000 : 0));
  return `${shifted.getUTCFullYear()}-${String(shifted.getUTCMonth()+1).padStart(2,"0")}-${String(shifted.getUTCDate()).padStart(2,"0")}T${String(shifted.getUTCHours()).padStart(2,"0")}:${String(shifted.getUTCMinutes()).padStart(2,"0")}`;
}
export function formatContractTime(seconds: number, zone: DisplayZone = zonePreference()): string {
  return new Intl.DateTimeFormat("en-GB", { dateStyle:"medium", timeStyle:"short", timeZone: zone === "UTC" ? "UTC" : "Europe/Lagos" }).format(new Date(seconds*1000)) + ` ${zone}`;
}
export function durationSeconds(value: number, unit: "Minutes"|"Hours"|"Days"): number {
  const factor = unit === "Minutes" ? 60 : unit === "Hours" ? 3600 : 86400;
  if (!Number.isFinite(value) || value < 0) throw new Error("Enter a non-negative duration.");
  return Math.floor(value * factor);
}

