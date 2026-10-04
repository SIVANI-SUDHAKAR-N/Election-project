import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = 'C:/Users/IND1/Desktop/project';
const buildDir = path.join(workspaceDir, '.janmat-pptx-work');
const outDir = path.join(workspaceDir, 'presentation-output');
const draftPath = path.join(buildDir, 'janmat-draft.pptx');
const finalPath = path.join(outDir, 'Janmat_Project_Presentation.pptx');
const skillDir = 'C:/Users/IND1/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
await fs.mkdir(buildDir, {recursive:true}); await fs.mkdir(outDir, {recursive:true});
const font = resolvePresentationFont({fontFamily:'Aptos'});
const C = {paper:'#F4F0E5', ink:'#17332E', green:'#246B57', orange:'#F06442', yellow:'#EBCB59', pale:'#DCE7DA', white:'#FFFDF7', muted:'#5A6C62', black:'#172421'};
const pres = Presentation.create({slideSize:{width:1280,height:720}});
function box(slide, text, x,y,w,h, size=24, color=C.ink, opts={}) {
  const s=slide.shapes.add({geometry:'textbox',name:opts.name||'text',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  s.text=text; s.text.style={typeface:font,fontSize:size,color,bold:!!opts.bold,alignment:opts.align||'left',verticalAlignment:opts.valign||'middle',autoFit:'shrink',wrap:true}; return s;
}
function base(bg=C.paper) { const s=pres.slides.add(); s.background.fill=bg; return s; }
function footer(slide, n, dark=false) { box(slide,'JANMAT  /  ELECTION SYSTEM',72,674,450,20,12,dark?C.pale:C.muted,{bold:true}); box(slide,String(n).padStart(2,'0'),1160,674,48,20,13,dark?C.pale:C.muted,{align:'right',bold:true}); }
function title(slide, kicker, heading, dark=false) { box(slide,kicker.toUpperCase(),74,48,900,25,15,dark?C.yellow:C.green,{bold:true}); box(slide,heading,72,88,1136,66,39,dark?C.white:C.ink,{bold:true}); }
function note(slide, text) { slide.speakerNotes.textFrame.setText(text); }

// 1. A restrained title with playful typographic ballot motif.
{
 const s=base(C.ink);
 box(s,'JANMAT',76,56,500,30,17,C.yellow,{bold:true});
 box(s,'A vote is\na promise.',72,150,730,235,76,C.white,{bold:true});
 box(s,'A small election platform with two ways to run the vote',78,418,760,42,25,C.pale);
 box(s,'J',946,132,190,220,164,C.orange,{bold:true,align:'center'});
 box(s,'WEB DEMO  +  JAVA CONSOLE',80,595,700,28,16,C.yellow,{bold:true});
 box(s,'PROJECT PRESENTATION',80,636,700,24,13,C.pale);
 note(s,'Janmat is documented as a front-end demonstration of a community election. The repository also includes a Java console implementation.');
}
// 2. Simple, human problem framing.
{
 const s=base(); title(s,'THE IDEA','Make a local election easy to follow');
 box(s,'A voter needs a clear ballot, a simple way to submit it, and a visible count.',76,196,580,150,33,C.ink,{bold:true});
 box(s,'01',760,185,92,72,56,C.orange,{bold:true}); box(s,'Know who is running',867,194,330,54,25,C.ink,{bold:true});
 box(s,'02',760,303,92,72,56,C.green,{bold:true}); box(s,'Use one registered voter ID',867,312,350,54,25,C.ink,{bold:true});
 box(s,'03',760,421,92,72,56,C.orange,{bold:true}); box(s,'See the tally update',867,430,350,54,25,C.ink,{bold:true});
 box(s,'The experience is designed around the voter journey.',78,522,520,64,22,C.muted);
 footer(s,2); note(s,'This slide summarizes the product intent stated in the website and Java documentation.');
}
// 3. Two implementations.
{
 const s=base(C.pale); title(s,'TWO WAYS TO RUN IT','One idea, two editions');
 box(s,'01   BROWSER DEMO',78,194,470,38,17,C.green,{bold:true});
 box(s,'Janmat',78,246,470,78,54,C.ink,{bold:true});
 box(s,'A friendly, visual ballot\nLocal browser storage\nLive tally and receipt',82,345,470,160,25,C.ink);
 box(s,'02   JAVA CONSOLE',682,194,500,38,17,C.orange,{bold:true});
 box(s,'Election system',682,246,520,78,46,C.ink,{bold:true});
 box(s,'Command line voting flow\nVoter and candidate objects\nText results export',686,345,480,160,25,C.ink);
 box(s,'Pick the edition that fits the room: click-through demo or terminal session.',80,570,1070,38,20,C.muted);
 footer(s,3); note(s,'The browser version lives in index.html, styles.css and app.js. The Java console version uses Main and the election domain classes.');
}
// 4. Voting journey shown as editable process steps.
{
 const s=base(); title(s,'THE VOTING JOURNEY','A ballot in three moves');
 const xs=[92,470,848]; const nums=['01','02','03']; const heads=['Meet the candidates','Check the voter ID','Cast and count']; const desc=['Read names, parties,\nand short descriptions.','Enter a registered ID.\nThe demo checks eligibility.','Select one candidate.\nThe tally refreshes.'];
 for(let i=0;i<3;i++){
   box(s,nums[i],xs[i],198,116,90,62,i===1?C.green:C.orange,{bold:true});
   box(s,heads[i],xs[i],301,330,66,29,C.ink,{bold:true});
   box(s,desc[i],xs[i],382,320,108,22,C.muted);
 }
 box(s,'Voter → ballot → result',82,560,1000,44,25,C.green,{bold:true});
 footer(s,4); note(s,'The three-step sequence follows the website flow: inspect candidates, enter a voter ID and submit a selected candidate. The tally is recomputed from stored votes.');
}
// 5. Browser demonstration details.
{
 const s=base(C.ink); title(s,'BROWSER EDITION','Janmat lives in one browser',true);
 box(s,'The page is plain HTML, CSS and JavaScript.',78,196,570,84,32,C.white,{bold:true});
 box(s,'Candidate cards',82,324,290,46,25,C.yellow,{bold:true}); box(s,'Ballot form',82,394,290,46,25,C.pale,{bold:true}); box(s,'Results tally',82,464,290,46,25,C.orange,{bold:true});
 box(s,'Local storage keeps the election setup and votes on that device.',670,210,500,110,26,C.white);
 box(s,'The organiser can edit candidate and voter lists, then restore the sample election.',670,350,500,124,23,C.pale);
 box(s,'Try it: VOTER-001 to VOTER-006',670,518,500,56,21,C.yellow,{bold:true});
 footer(s,5,true); note(s,'The website documentation lists six sample voter IDs and explains that setup and votes remain in the current browser local storage.');
}
// 6. Java edition and clear internals.
{
 const s=base(); title(s,'JAVA EDITION','VotingManager keeps the rules together');
 box(s,'REGISTER',82,205,260,34,15,C.orange,{bold:true}); box(s,'Voters\nCandidates',82,257,280,116,30,C.ink,{bold:true});
 box(s,'VALIDATE',486,205,260,34,15,C.green,{bold:true}); box(s,'Window\nVoter ID\nCandidate ID\nRepeat vote',486,257,330,190,24,C.ink);
 box(s,'REPORT',920,205,260,34,15,C.orange,{bold:true}); box(s,'Ranked results\nTie or winner\nText export',920,257,300,170,24,C.ink);
 box(s,'VoteStatus makes rejected ballots explicit.',82,526,600,45,24,C.green,{bold:true});
 box(s,'ACCEPTED   ·   UNKNOWN VOTER   ·   ALREADY VOTED   ·   WINDOW CLOSED',82,585,1110,28,15,C.muted,{bold:true});
 footer(s,6); note(s,'VotingManager handles registration, vote validation, synchronization of castVote, result calculation and vote storage. ResultsExporter writes voting-results.txt.');
}
// 7. Engineering choices grounded in code.
{
 const s=base(C.pale); title(s,'UNDER THE HOOD','Small choices that make the flow safer');
 box(s,'escapeHtml()',84,205,380,50,29,C.green,{bold:true}); box(s,'Escapes candidate-supplied text before it enters HTML.',84,261,430,100,21,C.ink);
 box(s,'Synchronized vote',660,205,460,50,29,C.orange,{bold:true}); box(s,'The Java manager protects the one-vote check and record operation.',660,261,490,100,21,C.ink);
 box(s,'Clock',84,432,380,50,29,C.orange,{bold:true}); box(s,'The Java rules receive a Clock, which keeps time checks testable.',84,488,450,94,21,C.ink);
 box(s,'Sorted results',660,432,460,50,29,C.green,{bold:true}); box(s,'The Java summary ranks by vote count, then candidate name.',660,488,490,94,21,C.ink);
 footer(s,7); note(s,'These details are present in app.js and VotingManager.java. The browser app escapes candidate text before rendering dynamic markup.');
}
// 8. Honest scope / limitations.
{
 const s=base(C.paper); title(s,'SCOPE CHECK','A demo election, with demo-level trust');
 box(s,'Works well for',82,202,400,48,28,C.green,{bold:true});
 box(s,'Presenting a voting flow\nTrying the interface locally\nExploring Java election rules',82,273,460,168,23,C.ink);
 box(s,'Not built for',670,202,440,48,28,C.orange,{bold:true});
 box(s,'Secure real elections\nShared results across devices\nVerified identity or tamper resistance',670,273,500,168,23,C.ink);
 box(s,'Browser data stays in that browser. Anyone with access can alter the local setup or stored votes.',82,515,1080,68,21,C.muted,{bold:true});
 footer(s,8); note(s,'The project website explicitly describes itself as a front-end demo, and states that local storage is not a secure election database and does not sync across devices.');
}
// 9. Demo script for a classroom or project review.
{
 const s=base(C.ink); title(s,'LIVE DEMO','A quick run-through',true);
 box(s,'01',82,200,90,66,52,C.yellow,{bold:true}); box(s,'Open index.html',192,202,480,52,28,C.white,{bold:true});
 box(s,'02',82,310,90,66,52,C.orange,{bold:true}); box(s,'Choose a candidate and enter VOTER-001',192,312,820,52,25,C.white,{bold:true});
 box(s,'03',82,420,90,66,52,C.green,{bold:true}); box(s,'Show the receipt and refreshed tally',192,422,820,52,25,C.white,{bold:true});
 box(s,'04',82,530,90,66,52,C.yellow,{bold:true}); box(s,'Use organiser controls to reset the sample',192,532,820,52,25,C.white,{bold:true});
 footer(s,9,true); note(s,'The sample voter ID is documented in WEBSITE.md. The reset control restores the sample election and clears votes in local storage.');
}
// 10. A clear finish with practical next steps.
{
 const s=base(C.orange);
 box(s,'JANMAT',78,54,500,30,17,C.white,{bold:true});
 box(s,'Thanks!\nQuestions?',76,154,700,192,68,C.white,{bold:true});
 box(s,'A small election project with a clear next chapter.',82,390,860,42,27,C.ink);
 box(s,'NEXT IF THIS GROWS UP',82,497,430,28,16,C.ink,{bold:true});
 box(s,'Add a trusted backend, persistent database,\nverified authentication and audit controls.',82,536,930,78,23,C.white);
 box(s,'?',1005,167,170,170,112,C.yellow,{bold:true,align:'center'});
 box(s,'PROJECT PRESENTATION',82,655,500,20,12,C.ink,{bold:true});
 note(s,'The next steps are recommendations inferred from the documented demo limitations, not features currently implemented.');
}

const expectedSlideSizeEmu='12192000,6858000';
const fontPolicy={basis:'design',families:[font]};
const requirements={explicitTotalSlideCount:10,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[]};
await (await PresentationFile.exportPptx(pres)).save(draftPath);
const { exportSlidesToImages } = await import(pathToFileURL(path.join(skillDir,'container_tools/artifact_tool_utils.mjs')).href);
// Render each slide as a private QA artifact using the presentation renderer.
for(let i=0;i<pres.slides.items.length;i++){
  const blob=await pres.export({slide:pres.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const stagingDir=path.join(workspaceDir,'.codex-finalizer'); await fs.mkdir(stagingDir,{recursive:true});
const result=await finalizePresentation({...requirements,workspaceDir,candidatePath:draftPath,finalPath,pythonExecutable:'C:/Users/IND1/AppData/Local/Programs/Python/Launcher/py.exe',integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu',expectedSlideSizeEmu,'--validate-bullet-geometry','--validate-heading-fit'],fontPolicy,verifyArtifactToolImport:true,receiptPath:path.join(stagingDir,'janmat-presentation-validation.json')});
console.log(JSON.stringify({finalPath,slides:pres.slides.items.length, font, result},null,2));


