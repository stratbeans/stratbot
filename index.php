<?php

require 'vendor/autoload.php';
include 'bootstrap.php';

use stratbot\Models\Task;
use stratbot\Models\User;
use stratbot\Middleware\Logging as botLogging;

$app = new \Slim\App();
$app->add(new botLogging());


$app->post('/assign', function($request, $response, $args) {
	$_task = $request->getParsedBodyParam('employee_id','');
	if($_task!=="")
	{
		$task = new Task();
		$task->user_id = $_task;
		$task->status = 'open';
		$task->task_details = $request->getParsedBodyParam('task_details','');
		$task->deadline = date('Y-m-d H-i-s',strtotime($request->getParsedBodyParam('deadline','')));
		$task->manager_id = $request->getParsedBodyParam('manager_id','');
		$task->save();
		return $response->withStatus(201)->withJson(['ok'=>'true']);
	}
	else
	{
		return $response->withStatus(400)->withJson(["ok"=>'false']);
	}	
});

$app->post('/complete', function($request, $response, $args) {
	$task_id = $request->getParsedBodyParam('task_id','');
	$user_id = $request->getParsedBodyParam('user_id','');
	if($task_id != "" )
	{
		$temp = Task::where('task_id', $task_id)->get();
		if(count($temp)==0) {return $response->withStatus(201)->withJson(["ok"=>'false','alreadyClosed'=>'false','wrongUser'=>'false']);}
		if($temp[0]['status']==="closed")  {return $response->withStatus(201)->withJson(["ok"=>'false','alreadyClosed'=>'true','wrongUser'=>'false']);}
		if($temp[0]['user_id']!==$user_id) {return $response->withStatus(201)->withJson(["ok"=>'false','alreadyClosed'=>'false','wrongUser'=>'true']);}
		Task::where('task_id', $task_id)->update(['status'=>'closed']);
		return $response->withStatus(201)->withJson(['ok'=>'true','alreadyClosed'=>'false','wrongUser'=>'false']);
	}
	else
	{
		return $response->withStatus(201)->withJson(["ok"=>'false','alreadyClosed'=>'false','wrongUser'=>'false']);
	}
});

$app->get('/opentasks', function($request, $response, $args) {
	$_task = new Task();
	$_user = new User();	
	$tasks = Task::where('status','=','open')->get();
	$payload = [];
	$payload['tasks'] = [];
	foreach ($tasks as $_tsk) {
			$_user = User::select('user_name')->where('user_id','=',$_tsk->user_id)->get();
			$_uname = '';
			if(count($_user)>0) {$_uname = $_user[0]['user_name'];}
			if($_user==null || $_uname=='') {$_uname = "Unknown";}
			array_push($payload['tasks'],
									["task_id" => $_tsk->task_id, 
									"user_name" => (string)$_uname,
									"details" => $_tsk->task_details,
									"deadline"=> $_tsk->deadline,
								]);
	}
	return $response->withStatus(200)->withJson($payload);
});

$app->post('/showtask', function($request, $response, $args) {

	$task_id = $request->getParsedBodyParam('task_id','');

	if($task_id===""){ $response->withStatus(201)->withJson(['ok'=>'false']);}	
	
	$tasks = Task::where('task_id','=',$task_id)->get();

	if(count($tasks)==0){ $response->withStatus(201)->withJson(['ok'=>'false']);}
	
	$manager_name = 'Unknown';
	$employee_name = 'Unknown';

	$manager = User::where('user_id','=',$tasks[0]['manager_id'])->get();
	if(count($manager)>0) { $manager_name = $manager[0]['user_name'];}

	$employee = User::where('user_id','=',$tasks[0]['user_id'])->get();
	if(count($employee)>0) { $employee_name = $employee[0]['user_name'];}
		
	$payload = [];
	$payload['ok'] ='true';
	//$payload['details'] = [];
	$payload['details']= ['task_details' => $tasks[0]['task_details'],
							'user' => $employee_name,
							'deadline' => $tasks[0]['deadline'],
							'status' => $tasks[0]['status'],
							'manager' => $manager_name,
							'created_at' => $tasks[0]['created_at'],
	];
	return $response->withStatus(201)->withJson($payload);
});

$app->post('/employeetask', function($request, $response, $args) {
	$_task = new Task();
	$tasks = Task::where([
							['status','=','open'],
							['user_id','=',$request->getParsedBodyParam('employee_id')],
						])->get();
	$payload = [];
	$payload['tasks'] = [];
	foreach ($tasks as $_tsk) {
			array_push($payload['tasks'],[ "task_id" => $_tsk->task_id,
									"task_details" => $_tsk->task_details,
									"deadline"=> $_tsk->deadline
								]);
		

	}
	$payload['ok'] = 'true';
	return $response->withStatus(201)->withJson($payload);
});

$app->run();
