import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
const { Canvas, Image } = await import(pathToFileURL('C:/Users/IND1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/node_modules/skia-canvas/lib/index.mjs'));
const root='C:/Users/IND1/Desktop/project';
const source=`${root}/.janmat-pptx-work`;
const out=`${root}/output/pdf/Janmat_Project_Presentation.pdf`;
const w=960,h=540;
const canvas=new Canvas(w,h);
for(let i=1;i<=17;i++){
  const png=await fs.readFile(`${source}/expanded-${String(i).padStart(2,'0')}.png`);
  const img=new Image(); img.src=png;
  const ctx=i===1?canvas.getContext('2d'):canvas.newPage();
  ctx.fillStyle='#F4F0E5'; ctx.fillRect(0,0,w,h); ctx.drawImage(img,0,0,w,h);
}
await canvas.toFile(out);
console.log(out);


