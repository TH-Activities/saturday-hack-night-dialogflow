<?php

// ENTER PATH TO FILE
$file_path = $_SERVER["DOCUMENT_ROOT"] . "/";

// ENTER NAME OF FILE 
$file_name = "subscriber-list.txt";


if($_POST) {
	
    $subscriber_email = $_POST['email'];
	$subscriber_fhp_input = $_POST['phone'];
	$array = array();
    
    if( $subscriber_email == "" ) {
        
        $array["valid"] = 0;
        
    } else {

        if( !filter_var($subscriber_email, FILTER_VALIDATE_EMAIL) || $subscriber_fhp_input != "") {

            $array["valid"] = 0;
            $array["message"] = $varErrorValidation;

        } else {

            file_put_contents($file_path.$file_name, strtolower($subscriber_email)."\r\n", FILE_APPEND);

            if (file_exists($file_path.$file_name)) {   

                $array["valid"] = 1;

            } else {

                $array["valid"] = 0;

            }

        }
        
    }
	
	echo json_encode($array);

}

?>