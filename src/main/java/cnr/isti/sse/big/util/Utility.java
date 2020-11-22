package cnr.isti.sse.big.util;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.StringReader;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PublicKey;
import java.security.SignatureException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import javax.xml.XMLConstants;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.bind.ValidationEvent;
import javax.xml.bind.ValidationEventHandler;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cms.CMSException;
import org.bouncycastle.cms.CMSSignedData;
import org.bouncycastle.cms.SignerInformation;
import org.bouncycastle.cms.jcajce.JcaSimpleSignerInfoVerifierBuilder;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.util.Store;
import org.bouncycastle.util.StoreException;
import org.w3c.dom.Document;

import cnr.isti.sse.big.data.reply.rp.LogRP;
import cnr.isti.sse.big.data.riepilogomensile.Abbonamenti;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiEmessi;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiFissi;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiIVAPreassolta;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiIVAPreassoltaAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.AltriProventiGenerici;
import cnr.isti.sse.big.data.riepilogomensile.BigliettiAbbonamento;
import cnr.isti.sse.big.data.riepilogomensile.BigliettiAbbonamentoAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.Evento;
import cnr.isti.sse.big.data.riepilogomensile.OrdineDiPosto;
import cnr.isti.sse.big.data.riepilogomensile.Organizzatore;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAccesso;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAccessoIVAPreassolta;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.TitoliIVAPreassoltaAnnullati;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.data.transazioni.Transazione;



public class Utility {

	private static org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(Utility.class);


	public static byte[] fromFileToByteArray(File file) {
		try {
			return FileUtils.readFileToByteArray(file);
		} catch (IOException e) {
			System.err.println("Error while reading .p7m file!" + e);
		}
		return new byte[0];
	}

	public static void writeToLogTransazioni(LogTransazione DCT, String ipAddress, int num){
		JAXBContext jaxbCtx;
		try {
			jaxbCtx = javax.xml.bind.JAXBContext.newInstance(LogTransazione.class);

			Marshaller marshaller = jaxbCtx.createMarshaller();
			marshaller.setProperty(javax.xml.bind.Marshaller.JAXB_ENCODING, "UTF-8"); //NOI18N
			marshaller.setProperty(javax.xml.bind.Marshaller.JAXB_FORMATTED_OUTPUT, Boolean.TRUE);
			//marshaller.marshal(annotatedCollaborativeContentAnalysis, System.out);
			String timeStamp = new SimpleDateFormat("dd_MM_yyyy__HH_mm_ss").format(new Date());
			File theDir = new File("received_"+ipAddress);

			// if the directory does not exist, create it
			if (!theDir.exists()) {
				theDir.mkdir();
			}

			OutputStream os = new FileOutputStream( "received_"+ipAddress+"/RT_"+ipAddress+"_"+timeStamp+"_"+num+".xml" );

			marshaller.marshal( DCT, os );

		} catch (JAXBException | FileNotFoundException  e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			log.error(e);

		}
	}




	private static Document convertStringToDocument(String xmlStr) {
		try {

			DOMResult output = new DOMResult();
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			transformer.transform(new StreamSource(new StringReader(xmlStr)), output);

			return (Document) output.getNode();

		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	public static void writeTo(String DCT, String ipAddress, int num){

		try {


			String timeStamp = new SimpleDateFormat("dd_MM_yyyy__HH_mm_ss").format(new Date());
			File theDir = new File("received_"+ipAddress);

			// if the directory does not exist, create it
			if (!theDir.exists()) {
				theDir.mkdir();
			}

			String FILENAME = "received_"+ipAddress+"/RT_"+ipAddress+"_"+timeStamp+"_"+num+".xml";
			BufferedWriter bw = new BufferedWriter(new FileWriter(FILENAME));


			bw.write(DCT);
			bw.close();

		} catch (  IOException  e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			log.error(e);
		}
	}













	public static void validateXmlLogTransazione(Unmarshaller unmarshaller)  {
		try {

			//Setup schema validator
			InputStream xsdcorr = Utility.class.getClassLoader().getResourceAsStream("logTransazioni.xsd");
			String text = IOUtils.toString(xsdcorr, StandardCharsets.UTF_8.name());

			//	URL xsdUrlB = Utility.class.getClassLoader().getResource("xmldsig-core-schema.xsd");


			//	String xsd = text.replace("./xmldsig-core-schema.xsd", xsdUrlB.getPath());

			//	Source schemaSource = new StreamSource(xsdcorr);

			//	 Schema corrispettiviSchema = sf.newSchema(schemaSource);


			SchemaFactory schemaFactory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
			//---

			Schema schema = schemaFactory.newSchema(new StreamSource(new StringReader(text)));




			unmarshaller.setSchema(schema);
			unmarshaller.setEventHandler(new XmlValidationEventHandler());
		} catch (Exception e) {
			// TODO: handle exception
			log.error("XML non valido per xsd "+e.getMessage());
		}

	}

	public static void validateXmlSigillo(Unmarshaller unmarshaller)  {
		try {


			//Setup schema validator
			InputStream xsdcorr = Utility.class.getClassLoader().getResourceAsStream("LogSigillo.xsd");
			String text = IOUtils.toString(xsdcorr, StandardCharsets.UTF_8.name());



			SchemaFactory schemaFactory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
			//---
			Schema schema = schemaFactory.newSchema(new StreamSource(new StringReader(text), "xsdTop"));




			unmarshaller.setSchema(schema);
			unmarshaller.setEventHandler(new XmlValidationEventHandler());

		} catch (Exception e) {
			// TODO: handle exception
			log.error("XML non valido per xsd"+e.getMessage());
		}

	}




	public static ImmutableTriple<Integer, Integer, Integer>  check(LogTransazione logT) {
		log.info("********CHECK LOG******");
		List<Transazione> listT = logT.getTransazione();
		// TODO Auto-generated method stub
		int totCor = 0;
		int totPr = 0;
		int prog = 0;
		int numeroprogressivi = 0;
		for(Transazione t : listT ) {
			String p = t.getNumeroProgressivo();
			int progparsed = Integer.parseInt(p.trim());
			if(prog==0) {
				prog = progparsed;
			}
			if(prog!=progparsed) {
				log.error("Progressivo Mancante "+prog);
			}
			prog++;
			numeroprogressivi++;
			//log.info(p);
			if(t.getTitoloAccesso()!=null) {
				String c = t.getTitoloAccesso().getCorrispettivoLordo();
				//String i = t.getTitoloAccesso().getImportoFigurativo();
				String pr = t.getTitoloAccesso().getPrevendita();
				try {

					int ic = Integer.parseInt(c.trim());
					//	int ii = Integer.parseInt(i.trim());
					int ipr = Integer.parseInt(pr.trim());
					totCor = totCor + ic;
					totPr = totPr + ipr;
					//System.out.println(p);
					//System.out.println(c);
					//	log.info(i);
					//System.out.println(pr);

				}catch (Exception e) {
					// TODO: handle exception

				}
			}
			if(t.getAbbonamento()!=null) {

				String c = t.getAbbonamento().getCorrispettivoLordo();
				String pr = t.getAbbonamento().getPrevendita();
				try {

					int ic = Integer.parseInt(c.trim());
					int ipr = Integer.parseInt(pr.trim());
					totCor = totCor + ic;
					totPr = totPr + ipr;
					//System.out.println(p);
					//System.out.println(c);
					//System.out.println(pr);

				}catch (Exception e) {
					// TODO: handle exception
					log.error(e);
				}

			}
			/*if(t.getBigliettoAbbonamento()!=null) {

				String c = t.getBigliettoAbbonamento().getImportoFigurativo();
				String pr = t.getBigliettoAbbonamento().getPrevendita();
				try {

					int ic = Integer.parseInt(c.trim());
					int ipr = Integer.parseInt(pr.trim());
					//totCor = totCor + ic;
					//totPr = totPr + ipr;
					//System.out.println(p);
					//System.out.println(c);
					//System.out.println(pr);

				}catch (Exception e) {
					// TODO: handle exception
					log.error(e);
				}

			}*/
		}
		float totCorrispettivo = (float)totCor/100;
		log.info("Corrispettivo Lordo: "+ totCorrispettivo);
		float totPrevendita = (float)totPr/100 ;
		log.info("Prevendita Lordo: "+ totPrevendita);
		float tot = (float)totCor/100+totPr/100;
		log.info("Totale Lordo: "+ tot);

		log.info("Totale Progressivi: "+ numeroprogressivi);
		//System.out.println(totCor);
		//System.out.println(totPr);
		//System.out.println(totCor+totPr);
		return  ImmutableTriple.of(numeroprogressivi, totCor, totPr);

	}



	private boolean callVerP7s(InputStream fileFW,InputStream fileFirma ) {
		try {
			byte[] bytes = IOUtils.toByteArray(fileFW);

			byte[] bytesc = IOUtils.toByteArray(fileFirma);

			return  verifyPKCS7(bytes);


		}catch (Exception e) {
			System.out.println("Signature verification failed " + e.getMessage());
			log.info("Signature verification failed " + e.getMessage());
		}
		return false;
	}

	/**
	 * Verify a PKCS7 signature.
	 *
	 * @param byteArray the byte sequence that has been signed
	 * @param psi 
	 * @param contents the /Contents field as a COSString
	 * @param sig the PDF signature (the /V dictionary)
	 * @throws CertificateException
	 * @throws CMSException
	 * @throws StoreException
	 * @throws OperatorCreationException
	 */
	public static boolean verifyPKCS7(byte[] byteArray) {
		// inspiration:
		// http://stackoverflow.com/a/26702631/535646
		// http://stackoverflow.com/a/9261365/535646
		//CMSProcessable signedContent = new CMSProcessableByteArray(byteArray);
		try {
			CMSSignedData signedData = new CMSSignedData(byteArray);
			Store certificatesStore = signedData.getCertificates();
			Collection<SignerInformation> signers = signedData.getSignerInfos().getSigners();
			SignerInformation signerInformation = signers.iterator().next();
			Collection matches = certificatesStore.getMatches(signerInformation.getSID());
			X509CertificateHolder certificateHolder = (X509CertificateHolder) matches.iterator().next();
			X509Certificate certFromSignedData = new JcaX509CertificateConverter().getCertificate(certificateHolder);

			//log.info("certFromSignedData: " + certFromSignedData);

			/*CertificateInfo ci = new CertificateInfo();
        psi.certificateInfo = ci;
        ci.issuerDN = certFromSignedData.getIssuerDN().toString();
        ci.subjectDN = certFromSignedData.getSubjectDN().toString();

        ci.notValidAfter = certFromSignedData.getNotAfter();
        ci.notValidBefore = certFromSignedData.getNotBefore();

        ci.signAlgorithm = certFromSignedData.getSigAlgName();
        ci.serial = certFromSignedData.getSerialNumber().toString();

        String issuerDN = certFromSignedData.getIssuerDN().toString();

        LdapName ldapDN = new LdapName(issuerDN);
        for(Rdn rdn: ldapDN.getRdns()) {
            ci.issuerOIDs.put(rdn.getType(), rdn.getValue().toString());
        }

        ldapDN = new LdapName(ci.subjectDN);
        for(Rdn rdn: ldapDN.getRdns()) {
            ci.subjectOIDs.put(rdn.getType(), rdn.getValue().toString());
        }*/

			//certFromSignedData.checkValidity(sig.getSignDate().getTime());

			if (isSelfSigned(certFromSignedData)) {
				log.info("Certificate is self-signed, LOL!");
				// psi.isSelfSigned = true;
			} else {
				log.info("Certificate is not self-signed");
				//psi.isSelfSigned = false;
				// todo rest of chain
			}

			if (signerInformation.verify(new JcaSimpleSignerInfoVerifierBuilder().build(certFromSignedData))) {
				//System.out.println("Signature verified");
				log.info("Signature verified");
				return true;
				//psi.signatureVerified="YES";
			} else {
				System.out.println("Signature verification failed");
				log.info("Signature verified");
				// psi.signatureVerified="NO";
			}
		}catch (Exception e) {
			// TODO: handle exception
			log.error(e.getMessage());
			return false;
		}

		return false;
	}

	public static byte[] getData(final byte[] p7bytes) {
		CMSSignedData cms = null;
		try {
			cms = new CMSSignedData(p7bytes);
		} catch (CMSException e) {
			log.error("Error while converting bytes to CMSSignedData : " + e.getMessage(), e);
		}
		if( cms == null || cms.getSignedContent() == null) {
			return new byte[0];
		}
		return (byte[]) cms.getSignedContent().getContent();
	} 

	public static Store<X509CertificateHolder> getCert(final byte[] p7bytes) {
		CMSSignedData cms = null;
		try {
			cms = new CMSSignedData(p7bytes);
		} catch (CMSException e) {
			log.error("Error while converting bytes to CMSSignedData : " + e.getMessage(), e);
		}
		if( cms == null || cms.getSignedContent() == null) {
			return  null;
		}
		return  cms.getCertificates();
	} 

	/**
	 * Checks whether given X.509 certificate is self-signed.
	 */
	private static boolean isSelfSigned(X509Certificate cert) throws CertificateException, NoSuchAlgorithmException, NoSuchProviderException {
		try {
			// Try to verify certificate signature with its own public key
			PublicKey key = cert.getPublicKey();
			cert.verify(key);
			return true;
		} catch (SignatureException | InvalidKeyException sigEx) {
			return false;
		}
	}


	public static ImmutableTriple<Integer, Integer, Integer> getTitoliAnnullati(List<TitoliAnnullati> titoli) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliAnnullati titolo: titoli) {
			if(titolo.getCorrispettivoLordo()!=null)
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			if(titolo.getQuantita()!=null)
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			if(titolo.getPrevendita()!=null)
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
			titolo.getTipoTitolo().trim();
			titolo.getImportoPrestazione().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}


	public static ImmutableTriple<Integer, Integer, Integer> getTitoliAccesso(List<TitoliAccesso> titoli) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliAccesso titolo: titoli) {
			if(titolo.getCorrispettivoLordo()!=null)
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			if(titolo.getQuantita()!=null)
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			if(titolo.getPrevendita()!=null)
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());			titolo.getTipoTitolo().trim();
			titolo.getImportoPrestazione().trim();
			
			checkIVA(titolo);
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	private static boolean checkIVA(TitoliAccesso titolo) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		if(titolo.getCorrispettivoLordo()!=null)
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
		if(titolo.getQuantita()!=null)
			quantita += Integer.parseInt(titolo.getQuantita().trim());
		if(titolo.getPrevendita()!=null)
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
		
		int ivacorr = Integer.parseInt(titolo.getIVACorrispettivo().trim());
		int ivaprev = Integer.parseInt(titolo.getIVAPrevendita().trim());
		DecimalFormatSymbols symbols = DecimalFormatSymbols.getInstance();
		symbols.setDecimalSeparator('.');
		DecimalFormat df = new DecimalFormat("#.##", symbols);
	//	df.format(number)
		 double corr =  Double.parseDouble(df.format(corrispettivo/quantita ) )/100 ;
		
		 //double baseiscorporocorriva22 = Double.parseDouble(df.format(corr*100/122 ));
		double baseiscorporocorriva10 = Double.parseDouble(df.format(corr*100/110));
		
		
		ImmutableTriple<Double, Double, Double> basei = calcBaseImpIncidenza(100,corr,22,16);
		
		double ivac22 = Double.parseDouble(df.format(basei.middle*22/100));
		double ivac10 = Double.parseDouble(df.format(baseiscorporocorriva10*10/100));
		
		
		
		int ivaf10 = (int) (ivac10*quantita*100);
		int ivaf22 = (int) (ivac22*quantita*100);
		
		if((ivacorr != ivaf10) & (ivacorr != ivaf22) ) {
			log.error("IVa errata in "+titolo);
			if((ivacorr < ivaf10) & (ivacorr < ivaf22) ) {
				log.error("IVa Minore in "+titolo);
			}
		}
		
		//int scorporopreviva22 = ivaprev*100/122;
		//int scorporopreviva10 = ivaprev*100/110;

		return false;
		
	}
	
	private static ImmutableTriple<Double, Double, Double> calcBaseImpIncidenza(double incidenza, double lordo, double impostaIVA, double impostaintratt) {
		//divido il lordo in base all'incidenza
		double lordoincidenza = lordo*incidenza/100;
		// scoporo iva + imposta
		double baseimposta = lordoincidenza*100/(100+impostaIVA+impostaintratt);
		double imposta = baseimposta*impostaintratt/100;

		double baseimpiva = baseimposta + ((lordo-lordoincidenza)*100/(100+impostaIVA));
		double iva = baseimpiva*impostaIVA/100;
		
		DecimalFormatSymbols symbols = DecimalFormatSymbols.getInstance();
		symbols.setDecimalSeparator('.');
		DecimalFormat df = new DecimalFormat("#.##", symbols);
		
		return ImmutableTriple.of(Double.parseDouble(df.format(baseimposta)),Double.parseDouble(df.format( baseimpiva)), Double.valueOf(0));
		
	}

	public static ImmutableTriple<Integer, Integer, Integer> getTitoliAccessoIVAPreassolta(List<TitoliAccessoIVAPreassolta> titoliAccessoIVAPreassolta) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliAccessoIVAPreassolta titolo: titoliAccessoIVAPreassolta) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	public static ImmutableTriple<Integer, Integer, Integer> getTitoliIVAPreassoltaAnnullati(
			List<TitoliIVAPreassoltaAnnullati> titoliIVAPreassoltaAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliIVAPreassoltaAnnullati titolo: titoliIVAPreassoltaAnnullati) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static ImmutableTriple<Integer, Integer, Integer> getBigliettiAbbonamento(List<BigliettiAbbonamento> bigliettiAbbonamento) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(BigliettiAbbonamento titolo: bigliettiAbbonamento) {
			if(titolo.getImportoFigurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFigurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());
			titolo.getTipoTitolo();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}

	public static ImmutableTriple<Integer, Integer, Integer>  sumImmutableTriple(List<ImmutableTriple<Integer, Integer, Integer> > listImmutableTriple) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(ImmutableTriple<Integer, Integer, Integer>  im :listImmutableTriple) {
			int quant = (int)im.left;
			quantita+=quant;
			int cor = (int)im.middle;
			corrispettivo+=cor;
			int pr = (int)im.right;
			prevendita+=pr;
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}
	
	public static ImmutableTriple<Integer, Integer, Integer>  sumImmutableTripleBig(List<ImmutableTriple<BigInteger, BigInteger, BigInteger> > listImmutableTriple) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(ImmutableTriple<BigInteger, BigInteger, BigInteger>  im :listImmutableTriple) {
			int quant = (int)im.left.floatValue();
			quantita+=quant;
			int cor = (int)im.middle.floatValue();
			corrispettivo+=cor;
			int pr = (int)im.right.floatValue();
			prevendita+=pr;
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}



	public static ImmutableTriple<Integer, Integer, Integer> getBigliettiAbbonamentoAnnullati(
			List<BigliettiAbbonamentoAnnullati> bigliettiAbbonamentoAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(BigliettiAbbonamentoAnnullati titolo: bigliettiAbbonamentoAnnullati) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiFissi(List<AbbonamentiFissi> abbonamentiFissi) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiFissi titolo: abbonamentiFissi) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static LogRP check(List<Organizzatore> organizzatori) {
		List<ImmutableTriple<Integer, Integer, Integer>> rootv = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		List<ImmutableTriple<Integer, Integer, Integer>> roota = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

		List<ImmutableTriple<Integer, Integer, Integer>> labb = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		List<ImmutableTriple<Integer, Integer, Integer>> alabb = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		
		List<ImmutableTriple<Integer, Integer, Integer>> rootlabbbiglietto = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		List<ImmutableTriple<Integer, Integer, Integer>> rootalabbbiglietto = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

		for(Organizzatore organizzatore: organizzatori) {


			List<Abbonamenti> abb = organizzatore.getAbbonamenti();


			for(Abbonamenti a: abb) {

				labb.add(Utility.getAbbonamentiEmessi(a.getAbbonamentiEmessi()));
				alabb.add(Utility.getAbbonamentiAnnullati(a.getAbbonamentiAnnullati()));
				Utility.getAbbonamentiIVAPreassolta(a.getAbbonamentiIVAPreassolta());
				Utility.getAbbonamentiIVAPreassoltaAnnullati(a.getAbbonamentiIVAPreassoltaAnnullati());

			}
			log.info("Abbonamenti Emessi"+labb);
			log.info("Abbonamenti Annulli"+alabb);
			List<AltriProventiGenerici> provgen = organizzatore.getAltriProventiGenerici();

			List<Evento> leventi = organizzatore.getEvento();
			for(Evento evento :leventi ) {
				log.info(evento.getIntrattenimento());
				log.info(evento.getMultiGenere());
				List<OrdineDiPosto> ordinip = evento.getOrdineDiPosto();
				int numerotitoli = 0;
				List<ImmutableTriple<Integer, Integer, Integer>> limm = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
				List<ImmutableTriple<Integer, Integer, Integer>> alimm = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

				List<ImmutableTriple<Integer, Integer, Integer>> labbbiglietto = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
				List<ImmutableTriple<Integer, Integer, Integer>> alabbbiglietto = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

				
				for(OrdineDiPosto ordinp: ordinip) {
					List<TitoliAccesso> titoliaccesso = ordinp.getTitoliAccesso();
					limm.add(Utility.getTitoliAccesso(titoliaccesso));
					List<TitoliAnnullati> titoliAnnullati = ordinp.getTitoliAnnullati();
					alimm.add(Utility.getTitoliAnnullati(titoliAnnullati));
					List<TitoliAccessoIVAPreassolta> titoliAccessoIVAPreassolta = ordinp.getTitoliAccessoIVAPreassolta();
					//limm.add(Utility.getTitoliAccessoIVAPreassolta(titoliAccessoIVAPreassolta));
					List<TitoliIVAPreassoltaAnnullati> titoliIVAPreassoltaAnnullati = ordinp.getTitoliIVAPreassoltaAnnullati();
					//alimm.add( Utility.getTitoliIVAPreassoltaAnnullati(titoliIVAPreassoltaAnnullati));
					List<BigliettiAbbonamento> bigliettiAbbonamento = ordinp.getBigliettiAbbonamento();
					labbbiglietto.add( Utility.getBigliettiAbbonamento(bigliettiAbbonamento));
					List<BigliettiAbbonamentoAnnullati> bigliettiAbbonamentoAnnullati = ordinp.getBigliettiAbbonamentoAnnullati();
					alabbbiglietto.add(Utility.getBigliettiAbbonamentoAnnullati(bigliettiAbbonamentoAnnullati));
					List<AbbonamentiFissi> abbonamentiFissi = ordinp.getAbbonamentiFissi();
					limm.add(Utility.getAbbonamentiFissi(abbonamentiFissi));

				}
				ImmutableTriple<Integer, Integer, Integer> sum = Utility.sumImmutableTriple(limm);
				log.info("Vendite: [Quantità, LordoCorrispettivo, LordoPrevendita]  "+sum);
				rootv.add(sum);
				ImmutableTriple<Integer, Integer, Integer> asum = Utility.sumImmutableTriple(alimm);
				roota.add(asum);
				log.info("Annulli: [Quantità, LordoCorrispettivo, LordoPrevendita] "+asum);
				
				ImmutableTriple<Integer, Integer, Integer> sumba = Utility.sumImmutableTriple(labbbiglietto);
				log.info("Biglietti Abb Emissioni: [Quantità, Importo figurativo, LordoPrevendita]  "+sumba);
				rootlabbbiglietto.add(sumba);
				ImmutableTriple<Integer, Integer, Integer> asumba = Utility.sumImmutableTriple(alabbbiglietto);
				rootalabbbiglietto.add(asumba);
				log.info("Biglietti Abb Annulli: [Quantità, Importo figurativo, LordoPrevendita] "+asumba);
				
				
			}

		}

		ImmutableTriple<Integer, Integer, Integer> rootsumv = Utility.sumImmutableTriple(rootv);
		ImmutableTriple<Integer, Integer, Integer> rootsuma = Utility.sumImmutableTriple(roota);
		LogRP.TitoliAccesso titoliAccesso = new LogRP.TitoliAccesso(rootsumv, rootsuma);

		ImmutableTriple<Integer, Integer, Integer> rootsumav = Utility.sumImmutableTriple(labb);
		ImmutableTriple<Integer, Integer, Integer> rootsumaa = Utility.sumImmutableTriple(alabb);
		LogRP.Abbonamenti abb = new LogRP.Abbonamenti(rootsumav, rootsumaa);
		
		
		ImmutableTriple<Integer, Integer, Integer> rootsumabbbiglietto = Utility.sumImmutableTriple(rootlabbbiglietto);
		ImmutableTriple<Integer, Integer, Integer> rootsumaabbbiglietto = Utility.sumImmutableTriple(rootalabbbiglietto);
		LogRP.BigliettiAbbonamenti babb = new LogRP.BigliettiAbbonamenti(rootsumabbbiglietto, rootsumaabbbiglietto);

		LogRP l = new LogRP(titoliAccesso,abb,babb);

		return l;

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiIVAPreassoltaAnnullati(
			List<AbbonamentiIVAPreassoltaAnnullati> abbonamentiIVAPreassoltaAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiIVAPreassoltaAnnullati titolo: abbonamentiIVAPreassoltaAnnullati) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiIVAPreassolta(List<AbbonamentiIVAPreassolta> abbonamentiIVAPreassolta) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiIVAPreassolta titolo: abbonamentiIVAPreassolta) {
			if(titolo.getImportoFiqurativo()!=null)
				corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo());
			if(titolo.getQuantita()!=null)
				quantita += Integer.parseInt(titolo.getQuantita());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiAnnullati(List<AbbonamentiAnnullati> abbonamentiAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiAnnullati titolo: abbonamentiAnnullati) {
			if(titolo.getCorrispettivoLordo()!=null)
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			if(titolo.getQuantita()!=null)
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			if(titolo.getPrevendita()!=null)
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiEmessi(List<AbbonamentiEmessi> abbonamentiEmessi) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiEmessi titolo: abbonamentiEmessi) {
			if(titolo.getCorrispettivoLordo()!=null)
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			if(titolo.getQuantita()!=null)
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			if(titolo.getPrevendita()!=null)
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}

}
class XmlValidationEventHandler implements ValidationEventHandler {

	private  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(XmlValidationEventHandler.class);
	@Override
	public boolean handleEvent(ValidationEvent event) {
		log.error("\nEVENT");
		log.error("SEVERITY:  " + event.getSeverity());
		log.error("MESSAGE:  " + event.getMessage());
		log.error("LINKED EXCEPTION:  " + event.getLinkedException());
		log.error("LOCATOR");
		log.error("    LINE NUMBER:  " + event.getLocator().getLineNumber());
		log.error("    COLUMN NUMBER:  " + event.getLocator().getColumnNumber());
		//         System.out.println("    OFFSET:  " + event.getLocator().getOffset());
		//         System.out.println("    OBJECT:  " + event.getLocator().getObject());
		//         System.out.println("    NODE:  " + event.getLocator().getNode());
		//         System.out.println("    URL:  " + event.getLocator().getURL());
		//throw new WebApplicationException(Response.status(406).entity("").build());

		return true;
	}



}
