export function splitWords(text: string) {
  return text.split(/\s+/).filter(Boolean);
}