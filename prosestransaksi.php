<?php
	$conSqlite 	= new PDO('sqlite:mirror.db', '', '', array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,));
	$code_trx	= "192039". date('Ymdhis');
	$name		= "Client A";
	$code_pulse	= $_GET['code_pulse'];

	$result = $conSqlite->query("SELECT * FROM pulse WHERE code_pulse='".$code_pulse."'")->fetch(PDO::FETCH_NAMED);
	if ($result['status']=='tersedia') 
	{
		$c = $conSqlite->prepare("INSERT INTO trxClient(code_trx,name,code_pulse)VALUES(:code_trx,:name,:code_pulse)");
		$c->bindParam(":code_trx",$code_trx);
		$c->bindParam(":name",$name);
		$c->bindParam(":code_pulse",$code_pulse);
		$c->execute();
		sleep(3);
		echo "<script>
					alert('Permintaan transaksi berhasil dikirim.');
					window.location.href='transaksi.php';
					</script>";
	}
	else{
		echo "<script>
					alert('Permintaan transaksi gagal dikirim');
					window.location.href='transaksi.php';
					</script>";
	}