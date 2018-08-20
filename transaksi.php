<?php  
   $conSqlite = new PDO('sqlite:mirror.db', '', '', array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,));
?>
<!DOCTYPE html>
<html>
<head>
   <title>Transaksi Pulsa</title>
   <link rel="stylesheet" type="text/css" href="assets/css/bootstrap.css">
</head>
<body>
   <div class="container">
      <div class="col-xs-12 col-md-5">
         <h3 align="center">Tabel Pulsa</h3>      
         <table class="table table-striped table-bordered table-responsive">
            <thead>
               <th>Kode Pulsa</th>
               <th>Nama Paket</th>
               <th>Saldo</th>
               <th>Status</th>
               <th>Aksi</th>
            </thead>
            <tbody>
            <?php
               $result = $conSqlite->query("SELECT * FROM pulse"); 
               foreach ( $result as $row) {
            ?> 
                  <tr>
                     <td><?php echo $row['code_pulse']; ?></td>
                     <td><?php echo $row['name']; ?></td>
                     <td><?php echo $row['balance']; ?></td>
                     <td><?php echo $row['status']; ?></td>
                     <td><a href="prosestransaksi.php?code_pulse=<?php echo $row['code_pulse'];?>" class="btn btn-sm btn-success">Beli</a></td>
                  </tr>
            <?php } ?>
            </tbody>
         </table>
      </div>
      <div class="col-xs-12 col-md-7">
         <h3 align="center">Tabel Transaksi</h3>      
         <table class="table table-striped table-bordered table-responsive">
            <thead>
               <th>Kode Transaksi</th>
               <th>Nama Pemesan</th>
               <th>Kode Pulsa</th>
               <th>Waktu</th>
            </thead>
            <tbody>
            <?php
               $result = $conSqlite->query("SELECT * FROM trx"); 
               foreach ( $result as $row) {
            ?> 
                  <tr>
                     <td><?php echo $row['code_trx']; ?></td>
                     <td><?php echo $row['name']; ?></td>
                     <td><?php echo $row['code_pulse']; ?></td>
                     <td><?php echo $row['buy_at']; ?></td>
                  </tr>
            <?php } ?>
            </tbody>
         </table>
      </div>
   </div>
   
</body>
</html>

   
   