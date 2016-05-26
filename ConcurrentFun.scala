import scala.math.BigInt
import scala.io.Source
import scala.concurrent.Future
import scala.concurrent.ExecutionContext
import scala.concurrent.Await
import scala.concurrent.duration._
import scala.concurrent._

import java.util.concurrent.Executors
import java.util.concurrent.Executors.defaultThreadFactory


object ConcurrentFun {
	implicit val ec = new ExecutionContext {
	    val threadPool = Executors.newFixedThreadPool(1, defaultThreadFactory);

	    def execute(runnable: Runnable) {
	        threadPool.submit(runnable)
	    }

	    def reportFailure(t: Throwable) {}
	}

	def readFileConcurrent(fn: String)(implicit ec: ExecutionContext): Future[BigInt] = Future {
		println("start reading")
		val fc = Source.fromFile(fn).getLines.mkString
		println(fc.length)
		println("stop reading")
		BigInt(fc.length)
	}

	def doFactorialCalc(num: BigInt)(implicit ec: ExecutionContext): Future[BigInt] = {
		println("start fac")
		val fac = (BigInt(1) to num).product
		println("stop fac")
		Future(fac)
	}

	def readFileAndDoFac(fn: String, num:BigInt)(implicit ec: ExecutionContext): Future[List[BigInt]] = {
		Future.sequence(List(readFileConcurrent(fn), doFactorialCalc(num)))
	}

	// def readFileAndDoFacPairs(fn: String, num:BigInt)(implicit ec: ExecutionContext): Future[List[BigInt]] = {
	// 	val fseq = Future.sequence(List(doFactorialCalc(num), doFactorialCalc(num)))
	// 	Future.sequence(List(readFileConcurrent(fn), doFactorialCalc(num)))
	// }

	def main(args: Array[String]) {
		println("Threaded")
		val fseq = readFileAndDoFac("/Users/bhtucker/rc/concurrent/medium.log", BigInt(42221))
		Await.result(fseq, 8 seconds)
		System.exit(1)
	}

	// def main(args: Array[String]) {
	// 	println("Sync")
	// 	readFileAndDoFacPairs("/Users/bhtucker/rc/concurrent/medium.log", BigInt(42221))
	// }

}

