package cnr.isti.sse.big.util;

public class Verify {
	
	static String normalize(String pi)
	{
		return pi.replaceAll("[ \t\r\n]", "");
	}
	
	/**
	 * Returns the formatted PI. Currently does nothing but normalization.
	 * @param pi Raw PI, possibly with spaces.
	 * @return Formatted PI.
	 */
	static String format(String pi)
	{
		return normalize(pi);
	}
	
	/**
	 * Verifies the basic syntax, length and control code of the given PI.
	 * @param pi Raw PI, possibly with spaces.
	 * @return Null if valid, or string describing why this PI must be
	 * rejected.
	 */
	static String validate(String pi)
	{
		pi = normalize(pi);
		if( pi.length() == 0 )
			return "Empty.";
		else if( pi.length() != 11 )
			return "Invalid length.";
		if( ! pi.matches("^[0-9]{11}$") )
			return "Invalid characters.";
		int s = 0;
		for(int i = 0; i < 11; i++){
			int n = pi.charAt(i) - '0';
			if( (i & 1) == 1 ){
				n *= 2;
				if( n > 9 )
					n -= 9;
			}
			s += n;
		}
		if( s % 10 != 0 )
			return "Invalid checksum.";
		return null;
	}
	
	private static void test(String raw_cf, String exp_err)
	{
		String got_err = validate(raw_cf);
		if( ! ("" + got_err).equals("" + exp_err) )
				throw new RuntimeException("got validation: " + got_err);
	}
	
	private static void test() {
		test("", "Empty.");
		test("@@@", "Invalid length.");
		test("@@@@@@@@@@@", "Invalid characters.");
		test("00000+00000", "Invalid characters.");
		test("12345678901", "Invalid checksum.");
		test("00000000001", "Invalid checksum.");

		test("00000000000", null);
		test("44444444440", null);
		test("12345678903", null);
		test("74700694370", null);
		test("57636564049", null);
		test("19258897628", null);
		test("08882740981", null);
		test("4730 9842  806", null);
	}
	
	

}
