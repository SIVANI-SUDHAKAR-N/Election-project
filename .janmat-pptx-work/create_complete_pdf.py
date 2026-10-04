from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import HexColor
from pathlib import Path

OUT=Path(r'C:\Users\IND1\Desktop\project\output\pdf\Janmat_Complete_Project_Presentation.pdf')
W,H=960,540
PAPER='#F4F0E5'; INK='#17332E'; FOREST='#246B57'; PALE='#DCE7DA'; ORANGE='#F06442'; YELLOW='#EBCB59'; WHITE='#FFFDF7'; MUTED='#5A6C62'; DARK='#102823'; LINE='#B9C9BD'
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('Janmat | Complete Project Presentation')
c.setAuthor('Janmat Project')
c.setSubject('Abstract, objectives, architecture, implementation, testing and future work')
pn=0

def fill(color): c.setFillColor(HexColor(color)); c.rect(0,0,W,H,stroke=0,fill=1)
def txt(x,y,s,size=16,color=INK,font='Helvetica',align='left'):
    c.setFillColor(HexColor(color)); c.setFont(font,size)
    if align=='right': c.drawRightString(x,y,s)
    elif align=='center': c.drawCentredString(x,y,s)
    else: c.drawString(x,y,s)
def wrap(s,maxw,font='Helvetica',size=16):
    out=[]
    for p in s.split('\n'):
        if not p: out.append(''); continue
        line=''
        for word in p.split():
            t=(line+' '+word).strip()
            if stringWidth(t,font,size)<=maxw or not line: line=t
            else: out.append(line); line=word
        out.append(line)
    return out
def block(x,top,s,maxw,size=16,color=INK,font='Helvetica',lead=None):
    lead=lead or size*1.34; y=top
    for line in wrap(s,maxw,font,size): txt(x,y,line,size,color,font); y-=lead
    return y
def label(x,y,s,color=FOREST): txt(x,y,s.upper(),10,color,'Helvetica-Bold')
def footer(dark=False,source=''):
    fc=PALE if dark else MUTED
    c.setStrokeColor(HexColor(fc)); c.setLineWidth(.55); c.line(62,42,898,42)
    txt(64,24,'JANMAT  /  COMPLETE PROJECT PRESENTATION',8,fc,'Helvetica-Bold')
    if source: txt(487,24,'SOURCE  '+source,7,fc,'Helvetica')
    txt(896,24,f'{pn:02d}',8,fc,'Helvetica-Bold','right')
def page(bg=PAPER,kicker='',title='',dark=False,source=''):
    global pn
    pn+=1; fill(bg)
    if kicker: txt(64,489,kicker.upper(),10,YELLOW if dark else FOREST,'Helvetica-Bold')
    if title: block(62,449,title,836,30,WHITE if dark else INK,'Helvetica-Bold',36)
    footer(dark,source)
def nextpage(): c.showPage()
def rule(x1,y1,x2,y2,color=LINE,width=1):
    c.setStrokeColor(HexColor(color)); c.setLineWidth(width); c.line(x1,y1,x2,y2)
def arrow(x1,y1,x2,y2,color=FOREST):
    c.setStrokeColor(HexColor(color)); c.setFillColor(HexColor(color)); c.setLineWidth(2); c.line(x1,y1,x2,y2)
    # simple arrow head for requested architecture diagram
    c.line(x2,y2,x2-7,y2+4); c.line(x2,y2,x2-7,y2-4)
def node(x,y,w,h,title,body,bg=WHITE,accent=FOREST,fs=11):
    c.setFillColor(HexColor(bg)); c.setStrokeColor(HexColor(accent)); c.setLineWidth(1.4); c.roundRect(x,y,w,h,8,stroke=1,fill=1)
    txt(x+12,y+h-21,title,12,accent,'Helvetica-Bold')
    block(x+12,y+h-41,body,w-24,fs,INK,'Helvetica',fs*1.25)

# 1 Cover
pn+=1; fill(DARK)
txt(70,484,'JANMAT  /  THE PEOPLE\'S VOTE',13,YELLOW,'Helvetica-Bold')
block(66,376,'A small election,\nexplained completely.',760,58,WHITE,'Helvetica-Bold',68)
txt(72,213,'PROJECT PRESENTATION',14,ORANGE,'Helvetica-Bold')
txt(72,173,'Browser voting demo  +  Java console system',23,PALE)
block(72,127,'Abstract, objectives, system design, implementation, testing, challenges and future work.',750,15,WHITE,'Helvetica',21)
txt(892,267,'01',112,YELLOW,'Helvetica-Bold','right'); txt(892,228,'JANMAT',13,PALE,'Helvetica-Bold','right')
footer(True,''); nextpage()

# 2 Abstract
page(PAPER,'01 / Abstract','A local voting experience in two forms',source='README.md  WEBSITE.md')
block(82,352,'Janmat demonstrates a small election workflow: present candidates, identify an eligible voter, accept one selection and report the result.',775,21,INK,'Helvetica',30)
label(82,205,'Browser demo'); block(82,178,'A single-page HTML, CSS and JavaScript experience. It stores setup and ballots in the current browser.',350,15,MUTED,'Helvetica',22)
label(528,205,'Java console',ORANGE); block(528,178,'A command-line program with voter and candidate objects, a timed voting window and a text results export.',350,15,MUTED,'Helvetica',22)
block(82,82,'This is a learning/demo project. The repository contains no remote voting API or shared database.',780,14,FOREST,'Helvetica-Bold')
nextpage()

# 3 Problem statement
page(PALE,'02 / Problem statement','A simple election still needs clear rules',source='WEBSITE.md  DESIGN_DOCUMENT.md')
label(82,350,'Problem'); block(82,321,'A confusing ballot makes it hard for a participant to know who is running, whether their voter ID is accepted, and how the count changes.',765,20,INK,'Helvetica',29)
label(82,195,'Real-world idea'); block(82,166,'Small community elections need a readable ballot and a predictable vote flow. Janmat models that experience for demonstration.',360,16,MUTED,'Helvetica',23)
label(528,195,'Project response',ORANGE); block(528,166,'Candidate information, voter ID checks, one-vote handling, feedback and a visible tally.',350,16,MUTED,'Helvetica',23)
nextpage()

# 4 objectives and scope
page(PAPER,'02 / Objectives and scope','The project turns the idea into two runnable demos',source='WEBSITE.md  USER_MANUAL.md')
objectives=[('01','Present candidates clearly'),('02','Check that a voter ID is registered'),('03','Prevent repeat votes in each implementation'),('04','Show a current tally and election outcome'),('05','Export the Java result as text')]
for i,(n,s) in enumerate(objectives):
    y=362-i*55; txt(84,y,n,20,ORANGE if i%2==0 else FOREST,'Helvetica-Bold'); txt(148,y,s,17,INK,'Helvetica-Bold')
block(610,354,'IN SCOPE',220,11,FOREST,'Helvetica-Bold'); block(610,326,'Local browser demo and Java console program.',245,16,INK,'Helvetica',22)
block(610,241,'OUT OF SCOPE',220,11,ORANGE,'Helvetica-Bold'); block(610,213,'Shared online election, verified real-world identity and secure remote ballot storage.',245,16,INK,'Helvetica',22)
nextpage()

# 5 final system overview
page(DARK,'03 / Final system overview','Two local flows, no shared server',True,'app.js  Main.java')
node(78,267,350,126,'BROWSER DEMO','index.html + styles.css + app.js\nData stays in browser localStorage.',DARK,YELLOW,13)
node(532,267,350,126,'JAVA CONSOLE','Main + VotingManager + domain classes\nState stays in process memory.',DARK,ORANGE,13)
label(82,205,'Shared idea',YELLOW); block(82,177,'Candidate registration, voter eligibility, one ballot per voter ID and readable results.',760,17,WHITE,'Helvetica',24)
block(82,80,'The two editions do not call each other. Their data and rules are separate.',770,14,PALE,'Helvetica-Bold')
nextpage()

# 6 architecture diagram
page(PAPER,'04 / Architecture and design','Final architecture: two independent paths',source='index.html  app.js  Main.java  VotingManager.java')
label(82,380,'BROWSER PATH');
node(76,245,210,100,'VOTER','Opens local page\nSelects candidate',WHITE,ORANGE,11)
node(375,245,220,100,'WEB APP','HTML / CSS / JS\nChecks and renders',WHITE,FOREST,11)
node(687,245,210,100,'LOCAL STORAGE','Election setup\nVotes and receipts',WHITE,ORANGE,11)
arrow(286,294,370,294); arrow(595,294,682,294)
label(82,190,'JAVA PATH',ORANGE)
node(76,72,168,85,'OPERATOR','Console input',WHITE,ORANGE,10)
node(283,72,168,85,'MAIN','Setup and output',WHITE,FOREST,10)
node(490,72,184,85,'VOTING MANAGER','Rules and state',WHITE,ORANGE,10)
node(713,72,184,85,'RESULTS EXPORTER','Text report',WHITE,FOREST,10)
arrow(244,114,278,114); arrow(451,114,485,114); arrow(674,114,708,114)
nextpage()

# 7 components / pattern
page(PALE,'04 / Architecture and design','Responsibilities stay in separate modules',source='app.js  Main.java  VotingManager.java')
mods=[('UI','index.html + styles.css','Page structure and visual presentation'),('Browser logic','app.js','State, validation, rendering and local persistence'),('Console entry','Main.java','Prompts, registration and user-facing result'),('Election rules','VotingManager.java','Eligibility, time window, vote recording and ranking'),('Domain objects','Voter, Candidate, Vote','Election state and accepted ballot data'),('Reporting','ResultsExporter.java','Text output from an ElectionResult')]
for i,(a,b,d) in enumerate(mods):
    x=80 if i%2==0 else 518; y=360-(i//2)*104
    label(x,y,a,ORANGE if i%2==0 else FOREST); txt(x,y-26,b,14,INK,'Helvetica-Bold'); block(x,y-48,d,350,12,MUTED,'Helvetica',16)
nextpage()

# 8 design practices
page(PAPER,'04 / Architecture and design','Patterns and practices visible in the code',source='VotingManager.java  ResultsExporter.java  app.js')
practice=[('Separation of concerns','UI, voting rules and export each have a clear home.'),('Domain model','Voter, Candidate and Vote describe election concepts.'),('Manager/service','VotingManager centralizes Java election operations.'),('Injected Clock','Time is supplied as a dependency for controllable time checks.'),('Synchronized operation','castVote() guards the check-and-record sequence.'),('Honest pattern note','No named GoF pattern is claimed in the project docs.')]
for i,(h,d) in enumerate(practice):
    y=361-i*51; txt(82,y,h,15,FOREST if i%2==0 else ORANGE,'Helvetica-Bold'); txt(328,y,d,13,INK)
nextpage()

# 9 UML diagram
page(PALE,'04 / UML class diagram','Java domain model and relationships',source='Java source classes')
# UML boxes: x,y,w,h,title,fields,methods
boxes={
 'voter':(65,305,205,112,'Voter','- id: String\n- name: String\n- hasVoted: boolean','+ hasVoted()\n+ markVoted()'),
 'candidate':(65,125,205,130,'Candidate','- id: String\n- name: String\n- politicalParty: String\n- voteCount: int','+ recordVote()'),
 'manager':(365,235,235,180,'VotingManager','- voters: Map\n- candidates: Map\n- votes: List\n- opening / closing time','+ registerVoter()\n+ registerCandidate()\n+ castVote()\n+ results()'),
 'vote':(365,80,235,110,'Vote','- voter: Voter\n- candidate: Candidate\n- timestamp: Instant','+ getters'),
 'result':(690,305,205,112,'ElectionResult','- ranked candidates\n- leaders\n- totalVotes\n- generatedAt','+ hasVotes()\n+ isTie()'),
 'receipt':(690,155,205,110,'VoteReceipt','- status: VoteStatus\n- processedAt\n- message','+ isAccepted()'),
 'exporter':(690,65,205,70,'ResultsExporter','+ exportTextReport()','')}
# relationship lines drawn behind boxes
rule(270,356,365,356,FOREST,1.2); rule(270,356,300,356,FOREST,1.2); rule(300,356,300,397,FOREST,1.2); rule(300,397,365,397,FOREST,1.2)
rule(270,190,335,190,FOREST,1.2); rule(335,190,335,280,FOREST,1.2); rule(335,280,365,280,FOREST,1.2)
rule(482,235,482,190,ORANGE,1.2)
rule(600,360,690,360,FOREST,1.2); rule(600,275,690,210,ORANGE,1.2); rule(792,305,792,135,FOREST,1.2)
# relation labels
label(286,365,'1..*',FOREST); label(301,202,'1..*',FOREST); label(488,210,'creates',ORANGE); label(610,368,'snapshot',FOREST); label(610,239,'receipt',ORANGE); label(798,191,'exports',FOREST)
for key,(x,y,w,h,title,fields,methods) in boxes.items():
    c.setFillColor(HexColor(WHITE)); c.setStrokeColor(HexColor(FOREST if key in ('voter','result','exporter') else ORANGE)); c.setLineWidth(1); c.rect(x,y,w,h,stroke=1,fill=1)
    txt(x+7,y+h-14,title,9,INK,'Helvetica-Bold'); rule(x,y+h-20,x+w,y+h-20,LINE,.5)
    yy=y+h-33
    for line in fields.split('\n') if fields else []: txt(x+7,yy,line,7.2,MUTED,'Helvetica'); yy-=10
    if methods: rule(x,y+30,x+w,y+30,LINE,.5); yy=y+20
    for line in methods.split('\n') if methods else []: txt(x+7,yy,line,7.2,FOREST,'Helvetica'); yy-=9
block(66,48,'Manager owns registries and accepted votes. Vote links a voter to a candidate. ResultsExporter writes the result snapshot.',820,9,MUTED)
nextpage()

# 10 core features
page(PAPER,'05 / Core features implemented','The platform covers the full demo loop',source='app.js  Main.java  VotingManager.java')
features=[('BALLOT','Candidate cards and single selection'),('ELIGIBILITY','Registered voter ID checks'),('ONE VOTE','Repeat ballot prevention'),('FEEDBACK','Receipt or reason for rejection'),('LIVE VIEW','Browser tally; Java summary'),('OUTCOME','No-vote, tie or winner result'),('SETUP','Edit or restore browser sample'),('EXPORT','Java writes voting-results.txt')]
for i,(a,b) in enumerate(features):
    col=i//4; row=i%4; x=84+col*430; y=365-row*68
    txt(x,y,a,11,ORANGE if row%2==0 else FOREST,'Helvetica-Bold'); block(x+125,y,b,260,14,INK,'Helvetica',18)
nextpage()

# 11 frontend implementation
page(PALE,'06 / Technical implementation: frontend','Browser UI is a static single-page app',source='index.html  styles.css  app.js')
label(82,354,'Markup'); block(82,328,'Sections for candidates, ballot, results and organiser controls. Forms use labels and required fields.',350,15,INK,'Helvetica',22)
label(528,354,'Styling',ORANGE); block(528,328,'styles.css controls the visual system and responsive layouts.',340,15,INK,'Helvetica',22)
label(82,198,'JavaScript'); block(82,172,'app.js loads the sample or saved election, handles form submissions, validates input, recomputes the tally and updates the page.',350,15,INK,'Helvetica',22)
label(528,198,'Accessible feedback',ORANGE); block(528,172,'Receipt and toast regions use status/live announcements. Candidate content is escaped before HTML insertion.',340,15,INK,'Helvetica',22)
block(82,78,'No frontend framework, package.json or build step is required. Open index.html in a modern browser.',790,13,FOREST,'Helvetica-Bold')
nextpage()

# 12 web logic/data
page(PAPER,'06 / Technical implementation: frontend','Browser data and matching rules',source='app.js')
label(82,353,'Local storage key'); txt(82,323,'janmat-election-v1',20,INK,'Courier-Bold')
block(82,267,'Stored data: candidates, voter IDs and vote records with voterId, candidateId, receiptCode and time.',360,15,INK,'Helvetica',23)
label(528,353,'Input behavior',ORANGE); block(528,323,'Voter IDs match without regard to case. Candidate IDs must be unique without regard to case during organiser setup.',345,15,INK,'Helvetica',23)
block(528,226,'Counts are rebuilt from saved vote records on each render. A sample election is used when saved data cannot be read.',345,14,MUTED,'Helvetica',20)
block(82,98,'Browser data is local to that browser profile and does not synchronize across visitors or devices.',780,14,MUTED,'Helvetica-Bold')
nextpage()

# 13 java specifics
page(PALE,'06 / Technical implementation: Java','Java runs as a local console application',source='Main.java  VotingManager.java')
label(82,354,'Setup'); block(82,328,'Main reads a positive duration, candidate details and registered voter details from the console.',350,15,INK,'Helvetica',22)
label(528,354,'Java baseline',ORANGE); block(528,328,'The user manual specifies JDK 11 or later. Compile with javac *.java and run java Main.',340,15,INK,'Helvetica',22)
label(82,197,'Rule engine'); block(82,171,'VotingManager stores voters and candidates in LinkedHashMaps, votes in a list, and receives a Clock.',350,15,INK,'Helvetica',22)
label(528,197,'ID handling',ORANGE); block(528,171,'Input IDs are trimmed. Map lookups preserve case, so V1 and v1 are distinct IDs.',340,15,INK,'Helvetica',22)
nextpage()

# 14 Java vote rules/time
page(PAPER,'06 / Technical implementation: Java logic','A ballot passes five checks')
checks=[('01','Window open'),('02','Voter registered'),('03','Voter has not voted'),('04','Candidate exists'),('05','Record Vote, increment count and mark voter')]
for i,(n,h) in enumerate(checks):
    y=366-i*57; txt(86,y,n,20,ORANGE if i%2==0 else FOREST,'Helvetica-Bold'); txt(150,y,h,16,INK,'Helvetica-Bold')
block(545,357,'castVote() is synchronized. The time window includes its exact closing instant.',320,16,INK,'Helvetica-Bold',23)
block(545,256,'Implementation detail: openingTime is captured before candidate and voter setup. Setup time counts toward the configured duration.',320,14,MUTED,'Helvetica',21)
block(86,65,'VoteReceipt returns ACCEPTED, WINDOW_CLOSED, UNKNOWN_VOTER, ALREADY_VOTED or UNKNOWN_CANDIDATE.',780,13,FOREST,'Helvetica-Bold')
nextpage()

# 15 result and export
page(PALE,'06 / Technical implementation: Java results','Results include ranking, tie handling and export',source='ElectionResult.java  ResultsExporter.java')
label(82,354,'Result snapshot'); block(82,326,'Sorted candidates, leader list, total vote count and generated time.',355,16,INK,'Helvetica',24)
label(528,354,'Outcome'); block(528,326,'No accepted votes: no-vote outcome. Multiple top candidates: tie. Otherwise: winner.',340,16,INK,'Helvetica',24)
label(82,194,'Export file',ORANGE); txt(82,163,'voting-results.txt',20,INK,'Courier-Bold')
block(82,127,'UTF-8 report with generated time, totals, candidate IDs, names, parties, counts and final outcome.',780,14,MUTED)
nextpage()

# 16 db integration
page(DARK,'06 / Database integration','No database is used in this project',True,'WEBSITE.md  Java source')
label(82,352,'Browser edition',YELLOW); block(82,322,'Persists data in localStorage on the current browser. This survives reloads in that browser, but it is user-editable local data.',350,16,WHITE,'Helvetica',24)
label(528,352,'Java edition',ORANGE); block(528,322,'Stores election objects in memory while the process runs. No database or durable ballot store is connected.',350,16,WHITE,'Helvetica',24)
block(82,154,'There is no server API, database schema, migration, or cross-device synchronization in the repository.',770,16,PALE,'Helvetica',23)
nextpage()

# 17 testing and debugging
page(PAPER,'07 / Testing and debugging','Documented scenarios and repository checks',source='TEST_CASES.md  USER_MANUAL.md')
label(82,354,'Documented scenarios'); block(82,326,'Valid vote; repeat vote; unknown voter; unknown candidate; duplicate registration; closed window; tie; report export.',365,15,INK,'Helvetica',22)
label(528,354,'Checks run'); block(528,326,'Java sources compiled with javac -Xlint:all. app.js passed node --check. git diff --check passed.',340,15,INK,'Helvetica',22)
label(82,191,'Evidence boundary',ORANGE); block(82,163,'TEST_CASES.md describes expected outcomes. The repository does not contain an automated test harness or unit/integration suite.',780,15,MUTED,'Helvetica',22)
block(82,72,'The Java compiler emitted an environment warning for a missing C:\\flutter\\bin path; compilation succeeded.',780,11,MUTED)
nextpage()

# 18 challenges/solutions
page(PALE,'08 / Challenges and solutions','Code responses to the main engineering constraints')
rows=[('Repeated ballot','Browser checks saved votes; Java synchronizes check and record.'),('Unknown IDs','Each implementation rejects IDs not in its voter or candidate list.'),('Bad input','The browser validates candidate fields; Java prompts retry on blank or duplicate registration.'),('Untrusted text','escapeHtml() encodes dynamic candidate text before HTML rendering.'),('Election timing','Java injects Clock and returns a specific closed-window status.')]
for i,(a,b) in enumerate(rows):
    y=359-i*61; txt(82,y,a,14,ORANGE if i%2==0 else FOREST,'Helvetica-Bold'); block(285,y,b,590,14,INK,'Helvetica',19)
block(82,62,'These are design constraints and code responses visible in the implementation, not a claim about undocumented development history.',790,11,MUTED)
nextpage()

# 19 security / limits
page(PAPER,'08 / Challenges and solutions','The demo has clear security boundaries',source='WEBSITE.md  app.js')
label(82,354,'Implemented safeguards'); block(82,326,'HTML escaping; one-vote checks; Java time-window rule; explicit rejection statuses.',355,15,FOREST,'Helvetica',22)
label(528,354,'Limits'); block(528,326,'Browser state can be edited locally. IDs are not verified identities. Java data disappears when the process ends.',345,15,ORANGE,'Helvetica',22)
block(82,155,'The project documentation calls the website a front-end demo and says localStorage is not a secure election database.',780,17,INK,'Helvetica-Bold',25)
nextpage()

# 20 conclusion/outcomes
page(DARK,'09 / Conclusion and outcomes','The objectives are met at demonstration scale',True)
items=[('Candidate view','Implemented'),('Registered voter checks','Implemented in both demos'),('One-vote handling','Implemented in both demos'),('Results and outcome','Browser tally and Java summary'),('Persistent/shared operation','Not implemented')]
for i,(a,b) in enumerate(items):
    y=362-i*58; txt(85,y,a,17,WHITE,'Helvetica-Bold'); txt(610,y,b,15,YELLOW if i<4 else ORANGE,'Helvetica-Bold')
block(85,72,'Final status: a working local demonstration with a documented route toward a larger system.',770,15,PALE)
nextpage()

# 21 future work
page(PALE,'10 / Future work','A production path needs new infrastructure')
future=[('01','Choose a deployment and election operations model'),('02','Add trusted identity verification and server-side authorization'),('03','Use durable shared storage with access controls'),('04','Build auditable records, backups and recovery procedures'),('05','Expand automated tests for concurrency and failures'),('06','Review accessibility and usability with real participants')]
for i,(n,s) in enumerate(future):
    y=369-i*48; txt(84,y,n,19,ORANGE if i%2==0 else FOREST,'Helvetica-Bold'); txt(148,y,s,15,INK,'Helvetica-Bold')
block(84,66,'These ideas extend the current demo. They are not features already delivered.',780,12,MUTED,'Helvetica-Bold')
nextpage()

# 22 run guide
page(PAPER,'Presentation appendix / Demo guide','Run either implementation from the project folder',source='WEBSITE.md  USER_MANUAL.md')
label(82,355,'Browser'); block(82,323,'Open index.html. Cast a sample ballot using VOTER-001. Show the receipt and tally, then restore the sample election.',350,15,INK,'Helvetica',23)
label(528,355,'Java console',ORANGE); block(528,323,'Compile with javac *.java. Run java Main. Register candidates and voters, cast a ballot, type exit and inspect voting-results.txt.',350,15,INK,'Helvetica',23)
block(82,120,'Java requires JDK 11 or later. Browser sample IDs are VOTER-001 through VOTER-006.',780,14,MUTED)
nextpage()

# 23 close
pn+=1; fill(ORANGE)
txt(72,481,'JANMAT  /  THE PEOPLE\'S VOTE',13,WHITE,'Helvetica-Bold')
block(68,380,'A clear ballot.\nVisible rules.\nAn honest scope.',735,46,WHITE,'Helvetica-Bold',58)
txt(75,160,'THANK YOU',14,INK,'Helvetica-Bold'); txt(75,120,'Questions?',28,INK,'Helvetica-Bold')
txt(894,234,'23',92,YELLOW,'Helvetica-Bold','right'); footer(False,''); c.save()
print(OUT)
