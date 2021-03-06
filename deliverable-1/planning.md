# Team 3 - Matron
 > **This document will serve as a master plan between your team, your partner and your TA.**

## Product Details
 
#### Q1: What are you planning to build?

Our project involves building a system that allows users to create and edit to-scale virtual blueprints of hospital units/wings so that our backend API can be queried to find the relative distances between rooms. This system will then act as a plugin to an existing scheduling system that considers the distances we return in trying to optimize nurse's schedules to minimize total walking distance.

The motivation is that one's perceived workload has been shown to be a function of total distance walked on the job. This unnecessary walking in the current spatially-unoptimized nurse schedules may increase stress or cause burnout, in turn affecting patient outcomes.

Our system consists of an in-browser graph editing interface where users build a map of their hospital unit using nodes (labelled with room numbers/labels) and edges connecting them (representing hallways), and a backend API that is to be queried by the existing scheduling system. Accurate graph scaling is integral to the function of our system and as such, users are to upload blueprints of their hospital wing to use as reference for building their graph. If the user has no access to such blueprints they can attempt to build their graph on a blank canvas from memory. Such freehand graphs we assume will be improperly scaled and to remedy this, users can optionally load our website on their mobile phones and select the tour based map rescaling feature. Here they will be asked to physically walk between a select number of rooms corresponding to nodes they've drawn in their graph. The user will be asked to tap their phone at the start and end of each leg of the tour (when the depart and when they arrive). The measured time delta along the taken path will be used to rescale their graph to the "correct" proportions (or in such a way that minimizes the total error of all known edge lengths). This process can be undertaken multiple times to further minimize the overall timing error.

If all rooms are full, patients may occasionally be held in ad-hoc locations such as corridors. To account for this, users can easily load the saved graph of their unit and add labelled nodes/edges wherever they see fit. The existing scheduling system can then identify which patient is stored in what named location and utilize our system to devise a schedule that allows nurses to visit them whilst minimizing total walking distance. The system we're building thus has no knowledge of the patients or where they're held.

It's important to note that nurse schedules are very flexible and that nurses must use their best judgement in deciding which patients require urgent care. The schedules generated by the optimizer using our system are thus merely suggestions for what order to visit the handful of patients assigned to a particular nurse.

Hospital administrators can choose to deploy our combined systems on a unit-by-unit basis to trial the improvement in patient outcomes, nurse morale, etc.

#### Q2: Who are your target users?
   
Hospital managers/administrators in charge of scheduling their worker's tasks. Such users would naturally wish to improve the efficiency of their workforce and one means to that end is the minimization of their worker's stepcount via Matron. Managers would use Matron in place of their existing scheduling system and would interact with our specific plugin to review the graphs constructed by interns to check for mistakes or to optionally add nodes to the graph at the end of the shift to accommodate patients stored in ad hoc locations.

Hospital interns in a unit implementing Matron would spend the most time directly interacting with the graph editor portion of our plugin. They would be responsible for translating the physical layout of their workspace into a virtual graph and ensuring the accuracy of its edge lengths via blueprint reference or physical path timing. The Matron scheduling optimizer requires such graphs to produce time/step optimized schedules that benefit nurses and, by extension, managers and patients.

Finally, nurses who feel frustrated having to walk past rooms they must later visit will benefit from the full Matron system powered by our distance calculations. These users would rarely interact with our system outside of potentially adding nodes to again accommodate patients stored in ad hoc locations at the end of their shifts. However, these individuals will see by far the most benefit from our system via their now spatially optimized schedules printed by Matron at the start of their shift.

#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?
   
As far as we or our partner knows, there's currently no existing solution for the walk-time minimization of nurse schedules. Our system will enable such a solution to materialize by allowing scheduling systems to query the distance (in seconds) between a given room and all other rooms, or between two given rooms.

Currently, nurse schedules are utterly spatially unoptimized and at best, are based solely on patient-related factors like acuity, etc. as existing scheduling systems have no knowledge of the space in which their workers operate. Nurses must thus embark on an effectively random tour of patient rooms. Since the current scheduling scheme in most hospitals approximates a worst-case tour, the combined Matron system can thus only serve to improve matters.

We offer a user-friendly graph editor that allows non-technical users to easily build and edit virtual maps of physical spaces ontop of blueprint backdrops if available. The integrity of such maps is maintained by error checking heuristics that warn the user of inaccessible areas, unlabeled nodes, etc. and a version history that allows users to rollback mistakes saved into the map.

Uniquely, our system sports a robust and novel global edge-rescaling feature that dynamically stretches/contracts areas of the graph based on a select-few known edge lengths via force-driven simulations.

As explained in Q1, nurses are not obligated to follow their schedules exactly, and thus there exists an upper bound on the extent to which the combined Matron system can reduce the walk-time of nurses, but the bound is not known. As such, hospital administrators who wish to improve the health, morale, and efficiency of their nurses can choose to deploy the Matron system on a unit-by-unit basis to see what effect it has.

#### Q4: How will you build it?
 
The plugin will be built using Python and Flask for the backend, and HTML5 and Javascript for the interactive frontend interface. We will also use Neo4J as our DBMS, which is a non-relation graph-based database and will be hosted on Heroku. We will also be using the D3 Javascript library to create and render the graphs in the graph editor interface and use 3D-Force Graphs to automatically rescale them using error minimization heuristics on the known edge lengths.

High level components of our project consists of:

The webserver, which the existing scheduling software will be directly interacting with through an API. This webserver will be written with Python/Flask and will be responsible for serving our frontend webpages (graph editor, etc.), communicating with our database (to fetch saved graphs, etc.), and handling graph pathfinding logic.

Database (Neo4J) : Responsible for storing blueprint image files, and past/current versions of each graph the user has made (for rollback purposes) and related metadata.

A pattern that we would like to use is the DOA (data access object that we discussed in class) so that the DBMS can be swapped out later with minimal hassle.

Our main testing method is unittest. We will also use continuous integration method. This is to say, we will perform code reviews and manually deploy the app onto Heroku to examine the app and look for any bugs which can be seen from the U.I. level. We will only deploy master-branch/working-app onto Heroku primarily for partner demonstration purposes after it has been thoroughly tested and received approval from the main tester.

#### Q5: What are the user stories that make up the MVP?

  - As a user of the Matron API, I want to see the distances between a given room and all other rooms of a given type (patientroom, supplyroom, workstation, etc.) so my scheduling software knows how best to plan a nurses day.
      - Software gives options for different room labels, and remembers given labels for rooms.
      - User is able to obtain a list (ordered by increasing distance) of all rooms of a given type, given a starting room.
  - As a user of the Matron API, I want to be able to query the distance between any two known rooms so I can optimize a route that traverses a set of rooms.
      - The API user can request for the distance between any two rooms.
  - As an intern, I want to upload hospital blueprints so I can use them as reference for building a correctly-scaled graph of my unit.
      - User is able to upload a blueprint/floorplan and have it appear as a backdrop to the map-making tool.
  - As an intern without access to my unit's blueprints, I want to visually construct a graph of my unit using nodes marked with room label/number/type and edges connecting them so that the system knows what routes we can walk.
      - Have a zoomable/pannable canvas UI that nodes/edges can be drawn ontop of to construct a graph.
  - As an intern, I want to click a button to save my graph once I'm done editing it so my hard work is not lost.
      - User can save the graph and load it again later, with the click of a button.
      - Allow users to edit and then resave graphs they've previously worked on
  - As an intern, I want to scroll through the history of my unit's graph so I can rollback/undo a bad edit.
      - User can access and view a sidebar which shows previous versions, as well as the corresponding dates.
      - The graph can be reverted to any previous version by selecting from the sidebar.
  - As an intern with a badly drawn unit graph, I want to physically measure the time it takes to walk along the edges of my graph so that the system can rescale it to the correct proportions.
      - User can access a webpage from their phone to use the time-measurement tool.
      - Following instructions from the webpage, the user can press a button to log the time it takes to walk between rooms.
      - The graph is automatically scaled with the data given by the user.
  - As an intern, I want to be notified of obvious mistakes in my graph such as unlabeled rooms or inaccessible areas so I can correct them.
      - The software intelligently warns the user of possible errors, as well as where they are happening.
  - As an intern, I want to box-select multiple rooms/nodes in the graph and drag them around so I can more easily fix large multi-node scaling inaccuracies in my graph.
      - Have a box-select tool that lets the user click and drag to draw a box, once they let go all nodes in the box should be selected and can then be moved around as a group.
  - As an intern, I want to click on the graph editor canvas to create a new node and type in its room number/label so the system knows which physical room that node corresponds to.
      - With the node creation tool selected, clicking on the canvas should create a node and open a context menu that lets the user type in the name/number/label of that node/room.
  - As an intern, I want to set the type of a newly created node via a context-menu that lists the existing types (eg., patientroom, supplyroom, workstation) and has an option that allows me to add a new custom type via the keyboard.
      - After the user creates a node and enters it's label, a new context menu opens that lists the existing types of room (for convenience) and has an option to enter a new one.
  - As an intern, I want to click to open a pie menu to select the tool I'm currently using in the graph editor so I can quickly switch between adding nodes, box-selecting nodes, drawing edges, or editing room labels/numbers/types.
      - Create a pie context menu UI around the cursor to switch tools in the graph editor
  - As a hospital manager, I want to open the graphs of multiple distinct hospital units and draw edges between them so the schedules of nurses working across multiple units can be optimized.
      - Have a page that lists all the unit graphs and allows them to be imported into each other
----

## Process Details

#### Q6: What are the roles & responsibilities on the team?
 
* **Saad: Project Manager and Team Lead**
  * *Responsibilities:*
    * Overall team organization, including managing Trello board, Discord server, and leading team meetings
    * Continually assess each team member and their assigned tasks, similar to a Scrum master type role
    * Review tasks and stories to make sure partner's requirements are met
    * Review project structure holistically and ensure overall backend/frontend integration
    * In charge of any ML and AI based techniques used in backend, as well as possibly advising on design of Flask backend 
  * *Strengths:*
    * Python and related libraries such as Flask, numpy/scipy, matplotlib
    * AI and ML including PyTorch, neural networks, and probabilistic techniques
    * Agile methodologies including Scrum and Kanban 
  * *Weaknesses:*
    * UI and frontend, including HTML/CSS and JS
    * mobile app development, such as Android apps in Java and iOS apps in Swift
    * unit testing and test-driven development
* **Kavosh: Partner liaison, Graph scaling manager, Graph-editor UX designer**
  * *Responsibilities:*
    * Communicate with partner
    * Audio record meetings and upload/share files with team
    * Work on the graph based map building UI
    * Build the blueprint-unassisted map rescaler
      * Create a page that instructors the user to go on a tour of the unit (the graph MST)
      * Instructors user to tap at the start and end of each leg of the tour
      * Uses the recorded time deltas to correct the scaling on an existing map graph  
  * *Strengths:*
    * Javascript/Java/Python
    * Computer graphics/physics simulation
    * Theoretical comp sci, graph theory/algorithms
  * *Weaknesses:*
    * Documenting code
    * Flask
    * noSQL databases
* **Adit: Front-end developer, UX designer**
  * *Responsibilities:*
    * Designing and implementing visual and interactive elements, in particular responsible for all pages except for the graph builder interface.
    * Deciding the look and layout of the web application
  * *Strengths:*
    * Front end development HTML, CSS, JS, and graphic design
    * Good experience with databases SQL and noSQL
    * Experience with web development with MERN stack, django, and flask
  * *Weaknesses:*
    * GIT merging conflicts
    * Infrequent activity of group project discord, as well low proficiency with discord
    * No experience with development methodologies
* **Thomas: Back-end Routing, Cheerleader**
  * *Responsibilities:*
    * Handling routing of the information coming from the back-end 
    * Maintaining team morale and motivation
    * Creating test cases for back-end related routing and events
    * Debugging back-end related events
  * *Strengths:*
    * Experience with python, HTML, CSS, and JS.
    * Capable of handling flexible workloads and working on other parts of the project if required.
    * Thoroughly experienced with debugging personal and other individuals code.
  * *Weaknesses:*
    * Working with the foreign libraries and frameworks that will be used.
    * Handling GIT conflicts such as merging.
* **Ilan: Backend Logic Developer, Assistant Cheerleader**
  * *Responsibilities:*
    * Processing of data structures and back end logic
    * Ensuring correctness of product's algorithms
    * Debugging and creating test cases during development of back end logic
  * *Strengths:*
    * Strong experience in Python and OOP design patterns
    * Well-versed in data structures and algorithms to do with graph traversal and pathfinding
    * High standards for documentation and code cleanliness
  * *Weaknesses:*
    * Databases and web development
    * Advanced Git usage
    * Little experience in front end development
* **David: Database Manager**
  * *Responsibilities:*
    * Setting up and maintaining the product database
    * Creating the DAO for the project
    * Determining data structure design/representation
  * *Strengths:*
    * Database management (PostgreSQL and MongoDB)
    * Server implementation in node.js, flask
    * Python, Javascript
  * *Weaknesses:*
    * General front end design (HTML/CSS) and associated UI libraries (bootstrap, react, etc.)
    * Mobile development/programming (both android/iOS)
    * Testing and debugging
* **John: Tester and unittest assistant**
  * *Responsibilities:*
    * Writing unittests and making sure the unittests works for people who have already written it
    * Debugging if unittest does not work and refactoring
  * *Strengths:*
    * Able write in python, SQL, javascript, html/css.
    * Likes to test and debug code - (good ability to pay attention to details).
    * Experience in mobile android app development.
  * *Weaknesses:*
    * Overall little technical experience in web development.
    * Not much familiar with design patterns.
    * Not familiar with libraries used in front-end. 


#### Q7: What operational events will you have as a team?
   
We plan to have team meetings once a week that all members are required to attend either in person or by call. Through a two-stage voting process we've decided on Thursday 5-6 as our regular meeting time, as it was the time that worked for 6/7 of our group members. For the group members who can't make it, they will call in using Discord so they can still contribute to group discussions. The location may change, but it will generally be a group study room booked in advance by the team lead - we've found that larger rooms with whiteboards and tv screens help us organize better.

The main purpose of the meetings will be to update the team on our progress so far, and share any questions or concerns that any team members have about the project. We plan to use a less strict organizational methodology like Kanban, so weekly meetings to check in and ensure we're on track will be necessary to keep us organized. The team lead will be responsible for keeping meeting minutes for all meetings in a dedicated channel on our Discord server.

We also have our meetings with our project partner. These will be biweekly and online via Skype, as per our partner's preference. Depending on our availability, different amounts of the team may join, but we have a dedicated partner liaison who will be the one to schedule the meetings and speak to the partner. If nobody else can join, the partner liaison will be responsible for taking the group's concerns to the partner and bringing back information at the weekly team meetings.

The first meeting with our project partner was mainly to get everyone introduced to each other, and discuss the basics of his proposal. We mainly talked about the general idea about what he wanted to build, what existing software he's already using, and what kind of technology would be feasible for our project. Before this meeting, we were unsure of what kind of implementations we could move forward with, so this was extremely useful for us to help narrow down our options and have a more focused project. For example, we considered building an app that would be deployed to the nurses in the hospital, but the partner clarified the manager will integrate our app with the existing system to generate schedules and then disseminate the information to the nurses. We also established the meeting schedule and exchanged contact information.

The second meeting was conducted online before the due date of the first Deliverable. Here, we wanted to confirm all of our user stories and other product details we had written in the Deliverable. This meeting went quite quickly as the partner approved the majority of user stories we had come up, and the group had a good sense of the partner's goals of the product from the first meeting. As the group thinks of more user stories, the partner liaison continually confirms them with the partner via email but so far they've all been approved other than minor changes.
  
#### Q8: What artifacts will you use to self-organize?
   
Our team's primary means of internal communication is via Discord. Our group's server has 5 total text channels split into two categories:

Organizational: There are three text channels under this category that are used to make team-wide announcements, post meeting minutes, and share important notes as they come up. The first two are restricted so that only the project manager may post announcements and meeting minutes, to keep irrelevant conversations out of the way and better disseminate information. The last one serves as more of a queue to deal with items as they come up, and issues here will then be moved to the appropriate place such as on the Trello board.

Production: Two text channels here are used for general chat and issue discussion when it requires the attention of some or all other team members. This server provides a quick means of instant messaging between the group while still organizing messages into unique and useful categories. There are also 4 voice chat rooms which our team members may join at any time. We have multiple voice chat rooms so that members may split off into pairs or small groups and work on issues/files together.

For team-wide announcements, we use Discord's emoji reaction feature to verify the all team members have read and concur with the announcement. For example, if the project lead announces that we are to hold a meeting on date X, all members who can make it react with a thumbs up emoji and those who can't react with a thumbs down emoji. This reduces clutter on the message board as reactions are tied to the announcement and don't show up as unique messages. If a member doesn't react within 24 hours, we assume they haven't seen the announcement and will make further attempts to reach them.

When any vote needs to be done, we have various methods of polling the group members. For voting on meeting times, we use a service called when2meet which is designed to help groups determine who is busy and when to find the optimal meeting times. If there are any ties, we use a regular vote to tiebreak the most popular choices; this is the same two stage voting process we used to determine our weekly meeting time. For regular votes, we use Google forms as it is the most powerful option, and has useful features such as allowing anonymity  and filtering results. We previously used strawpoll for such things, but realized the built-in anonymity made it difficult to tell who exactly wasn't free to meet at certain times.

Our team also has a Trello board where we use a modified form of Kanban. We post important information (To-do lists, pending tasks, documentation, etc.) here as well for everybody to see. Group members can see when one member takes on a specific task, as well as when it is ready for design, implementation, testing, and code review. We plan to use this board to facilitate a modified version of Kanban; we will pipeline our code and features on a Kanban board, but with the added oversight of a scrum master type role to keep all team members focused and on track. 

#### Q9: What are the rules regarding how your team works?

We plan to have a fairly open working culture, where each team member is given a task or role and has freedom to handle it however they see fit. We've divided the project into general roles such as frontend, backend, database, etc. and each member will oversee and do any research, design, and implementation on any area they're in charge of. We'll have weekly meetings and consistent communication on our Discord server to ensure team members are organized and completing their tasks, and the team lead will oversee the Trello board to keep the project on track. When they merge a pull request to the master branch, we will require 3 code reviews to ensure only quality code is committed and that each team member has a sense of the overall state of the project.

**Communications:**
 
Between group members, minimum of once a week because we have a weekly meetings. On average, we expect to speak with each other regarding the project about once every other day via our Discord server or in person. For emergencies, we've all shared our phone numbers with each other except for 1 group member who didn't consent. Our expected frequency of communications with the partner is biweekly, as per the partners preference, with a Skype call or via email for immediate requests. We have a dedicated partner liaison who will be responsible for keeping the partner up to date on our progress and sending emails if we have any questions.

**Meetings:**
 
If a group member doesn't attend a meeting or complete an assigned action item, the team lead will contact them and ask for justification about why they didn't attend. We have various ways to contact each other if needed including our official Discord server, email, phone number, or just in person if needed. The team lead is willing to step in if needed, and in extreme cases the TA or course coordinators would be contacted to find a resolution. Since each team member has a distinct role, we take it seriously if they don't contribute since covering their workload would be quite difficult.
 
**Conflict Resolution:**

 * Team indecision:
      * In terms of development the first course of action would be to have a vote and see if there's a clear consensus. If not, then the team member(s) that are in charge of the implementation of the feature will have the final say in the design decision. If this is a decision we believe the partner would have insight on, we will contact them and they will have final say. This is because we believe that the person who has to actually code a feature should have more control over the specifications of that feature.
      * However, if we still cannot come to an agreement after we've thoroughly discussed all options we will leave it up to chance pick which one to choose.
   
 * Non-responsive team members:
     * If this were to occur, the plan is to attempt to contact the non-responsive team member; firstly via Discord and email, and then using their phone number and finding them in person. If this behavior were to continue for longer than 3 days, then we would contact our TA and course coordinator and let them know about this. 

 * Unproductive member: 
   Our policy can be broken down into two scenarios, based on the cause of the problem:
   * **Unforeseen circumstances:** In this case, the member is unable to fully contribute due to factors outside of our control. It would be unfair to penalize them for this. The team member with the greatest amount of availability and knowledge of the unproductive member's responsibility will take on their work until the unproductive member is able to fully contribute to the project again.
   * **Just unproductive/unresponsive:** A team member who is just not doing their part will be handled as described before. We will first contact them normally, through Discord, email, phone, or in person. If this does not help, the team lead and course coordinators may get involved.
----
### Highlights
 
The first issue that repeatedly came up was how we would gather data about the distances between rooms when said information was not given or known by the users. We had a variety of options for how we would gather this data including gps tracking, accelerometer data (step counting), and time measurements from something like a stopwatch or timer. Each of these had their various pros and cons. For example, gps tracking would give the most accurate distance information under ideal conditions but might be completely unfeasible deep inside large buildings (like a hospital). Accelerometer data is still fairly accurate to a degree and would not depend on the gps quality but would require some averaging to account for different peoples' strides. Time is the simplest metric and would not require use of separate hardware such as a gps unit or accelerometer. Ultimately, we decided on using time as the distance metric since 1. we wouldn't need to implement a mobile solution to gather the distance information 2. It would be able to account for additional factors like hallway traffic. 3. It's less dependent on external factors such as gps and accelerometer quality. 

Another issue that came up was what choice of database we would use to store our data. Our options were Postgres (SQL), MongoDB (noSQL) and Neo4j (NoSQL and Graph DB). The considerations for SQL vs noSQL were fairly standard (structure vs flexibility, efficiency vs scalability). The other option was considered specifically because of its applicability towards our project since our main functionality is specifically graph-related. Another consideration was our collective familiarity with the various types of databases. Overall, we were the most familiar with MongoDB, with Postgres being a close second. Meanwhile, none of us had any experience with Neo4j, which meant that we would have to learn how to use it from scratch. In the end, we chose to use Neo4J because we determined that the functionality it could provide for us outweighed the potential learning curve. We made this decision by having David, who is in charge of the database and interacting with it, do some research on the pros and cons of the various database options. He then presented each option to the group and after some discussion, we voted on which option we preferred. Since David would be the one interacting with the database the most and deciding how to design it, his vote was weighted higher. Luckily, we all came to a consensus on using Neo4j since its functionality would make it alot easier to implement our planned features. 

Another issue that repeatedly came up was how we would gather data about the distances between rooms and create the virtual blueprint. Our first idea revolved around tracking the time or the steps it would take nurses to walk from room to room with an app, and then create a graph that represents that data to feed into the pathfinding system. We were drawn to this idea because it seemed much more flexible and dynamic than manually inputting the blueprints or building a computer vision system. However, some team members reread the project proposal and realized this system wouldn't work to the specifications the partner described because an additional app would have to be distributed to the nurses. We deliberated this choice for a while and then realized there was no way to come to a consensus without consulting the project partner. So, we arranged the first meeting with our partner soon after that, and presented the two options to him: whether we could proceed with a step-counting/distance based approach and give an app to the nurses, or if we should build a system to manually input blueprints that will directly connect to the existing scheduling system. He confirmed that we could not distribute apps to the nurses, which allowed to focus on one main implementation idea and move forward with that.

Finally, another decision we made was to change our partners proposal slightly. Our partner had proposed the interface for mapping out the hospital floor plans would consist of a grid based system in which the user would add blocks, representing walls, rooms, hallways, etc. We instead took a decision to change it to a system were we would draw lines connecting hallways where rooms would be represented using nodes. The pro of the grid based system was the simplicity, however the con was that it would have difficulty modeling oddly shaped hallways. The benefit of the line segment based system we proposed was its versatility for mapping oddly shaped hallways, but at the cost of a slightly more complicated interface. In the end the decision we took was the line segment based graph builder, the key reason being that during our meeting with our partner, he brought along an physical copy of a floor plan, and we noticed there were oddly shaped hallways and rooms which would not be accurately modeled with a grid based system. Since the partner was non-technical, he did not oppose the change and he accepted our technical expertise when it came to design and implementation of features.
