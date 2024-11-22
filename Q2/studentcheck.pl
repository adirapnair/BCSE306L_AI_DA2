:- use_module(library(csv)).
:- use_module(library(http/json)).
:- use_module(library(http/http_server)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).

% Load CSV file
load_csv(File) :-
    csv_read_file(File, Rows, [functor(student), arity(3)]),
    maplist(assert, Rows).

% Eligibility rules
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_percentage, _),
    Attendance_percentage >= 75.

% HTTP Handlers
:- http_handler(root(scholarship), check_scholarship, []).
:- http_handler(root(exam), check_exam, []).

% Handler to check scholarship eligibility
check_scholarship(Request) :-
    http_parameters(Request, [id(Student_ID, [atom])]),
    ( eligible_for_scholarship(Student_ID) ->
        reply_json_dict(_{student: Student_ID, scholarship: "Eligible for scholarship"});
        reply_json_dict(_{student: Student_ID, scholarship: "Not Eligible for scholarship"})
    ).

% Handler to check exam permission
check_exam(Request) :-
    http_parameters(Request, [id(Student_ID, [atom])]),
    ( permitted_for_exam(Student_ID) ->
        reply_json_dict(_{student: Student_ID, exam: "Permitted for exam"});
        reply_json_dict(_{student: Student_ID, exam: "Not Permitted for exam"})
    ).

% Start the server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).