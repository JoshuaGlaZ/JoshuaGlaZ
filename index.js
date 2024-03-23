function generateOutput(progressPercentage) {
  const passedProgressBarIndex = Math.floor(progressPercentage * 63);
  const progressBar =
    "▓".repeat(passedProgressBarIndex) +
    "░".repeat(63 - passedProgressBarIndex);

  const asciiArt = `### Hey, I'm JoshuaGlaZ

- ☁ API & Github Action enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django, Next.js
- ☕ Preferred Coffee over Tea

\`\`\`text
'
'     ___       __       ___    __ __
'   /'___\`\\   /'__\`\\   /'___\`\\ /\\ \\\\ \\      
'  /\\_\\ /\\ \\ /\\ \\/\\ \\ /\\_\\ /\\ \\\\ \\ \\\\ \\     ▛▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
'  \\/_/// /__\\ \\ \\ \\ \\\\/_/// /__\\ \\ \\\\ \\_     ${progressBar} ${(progressPercentage * 100).toFixed(2)}%
'     // /_\\ \\\\ \\ \\_\\ \\  // /_\\ \\\\ \\__ ,__\\ ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▞
'    /\\______/ \\ \\____/ /\\______/ \\/_/\\_\\_/
'    \\/_____/   \\/___/  \\/_____/     \\/_/
'                                                                         📢 Updated on ${new Date(
    now
  ).toUTCString()}
'
\`\`\`
`;
  return asciiArt;
}

const now = Date.now();
const thisYear = new Date(now).getFullYear();
const startOfYear = new Date(thisYear, 0, 1);
const endOfYear = new Date(thisYear, 11, 31, 23, 59, 59);
const progressOfThisYear = (now - startOfYear) / (endOfYear - startOfYear);
console.log(generateOutput(progressOfThisYear));
