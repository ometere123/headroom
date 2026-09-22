export function formatAttoGen(raw: string | number | bigint): string {
  const value=BigInt(raw||0);const whole=value/10n**18n;const fraction=(value%10n**18n).toString().padStart(18,"0");const trimmed=fraction.replace(/0+$/g,"");return `${whole.toLocaleString()}${trimmed?`.`+trimmed:""} GEN`;
}

