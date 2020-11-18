package cnr.isti.sse.big.util;

import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.StringReader;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.Principal;
import java.security.PublicKey;
import java.security.SignatureException;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.naming.InvalidNameException;
import javax.security.auth.x500.X500Principal;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.xml.XMLConstants;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.bind.ValidationEvent;
import javax.xml.bind.ValidationEventHandler;
import javax.xml.crypto.dsig.Reference;
import javax.xml.crypto.dsig.XMLSignature;
import javax.xml.crypto.dsig.XMLSignatureFactory;
import javax.xml.crypto.dsig.dom.DOMValidateContext;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.asn1.x500.style.BCStyle;
import org.bouncycastle.asn1.x500.style.IETFUtils;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cms.CMSException;
import org.bouncycastle.cms.CMSProcessable;
import org.bouncycastle.cms.CMSProcessableByteArray;
import org.bouncycastle.cms.CMSSignedData;
import org.bouncycastle.cms.SignerInformation;
import org.bouncycastle.cms.jcajce.JcaSimpleSignerInfoVerifierBuilder;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.util.Store;
import org.bouncycastle.util.StoreException;
import org.glassfish.grizzly.utils.Pair;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import cnr.isti.sse.big.data.reply.rp.LogRP;
import cnr.isti.sse.big.data.riepilogomensile.*;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.data.transazioni.Transazione;
import javassist.expr.Instanceof;



public class Utility {

	private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(Utility.class);


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
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
			titolo.getTipoTitolo().trim();
			titolo.getImportoPrestazione().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}


	public static ImmutableTriple<Integer, Integer, Integer> getTitoliAccesso(List<TitoliAccesso> titoli) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliAccesso titolo: titoli) {
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());
			titolo.getTipoTitolo().trim();
			titolo.getImportoPrestazione().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	public static ImmutableTriple<Integer, Integer, Integer> getTitoliAccessoIVAPreassolta(List<TitoliAccessoIVAPreassolta> titoliAccessoIVAPreassolta) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliAccessoIVAPreassolta titolo: titoliAccessoIVAPreassolta) {
			corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	public static ImmutableTriple<Integer, Integer, Integer> getTitoliIVAPreassoltaAnnullati(
			List<TitoliIVAPreassoltaAnnullati> titoliIVAPreassoltaAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(TitoliIVAPreassoltaAnnullati titolo: titoliIVAPreassoltaAnnullati) {
			corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static ImmutableTriple<Integer, Integer, Integer> getBigliettiAbbonamento(List<BigliettiAbbonamento> bigliettiAbbonamento) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(BigliettiAbbonamento titolo: bigliettiAbbonamento) {
			corrispettivo += Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			titolo.getTipoTitolo().trim();
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



	public static ImmutableTriple<Integer, Integer, Integer> getBigliettiAbbonamentoAnnullati(
			List<BigliettiAbbonamentoAnnullati> bigliettiAbbonamentoAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(BigliettiAbbonamentoAnnullati titolo: bigliettiAbbonamentoAnnullati) {
			corrispettivo = Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita = Integer.parseInt(titolo.getQuantita().trim());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiFissi(List<AbbonamentiFissi> abbonamentiFissi) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiFissi titolo: abbonamentiFissi) {
			corrispettivo = Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita = Integer.parseInt(titolo.getQuantita().trim());
			titolo.getTipoTitolo().trim();
		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	public static LogRP check(List<Organizzatore> organizzatori) {
		List<ImmutableTriple<Integer, Integer, Integer>> rootv = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		List<ImmutableTriple<Integer, Integer, Integer>> roota = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

		List<ImmutableTriple<Integer, Integer, Integer>> labb = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		List<ImmutableTriple<Integer, Integer, Integer>> alabb = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

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

				for(OrdineDiPosto ordinp: ordinip) {
					List<TitoliAccesso> titoliaccesso = ordinp.getTitoliAccesso();
					limm.add(Utility.getTitoliAccesso(titoliaccesso));
					List<TitoliAnnullati> titoliAnnullati = ordinp.getTitoliAnnullati();
					alimm.add(Utility.getTitoliAnnullati(titoliAnnullati));
					List<TitoliAccessoIVAPreassolta> titoliAccessoIVAPreassolta = ordinp.getTitoliAccessoIVAPreassolta();
					//limm.add(Utility.getTitoliAccessoIVAPreassolta(titoliAccessoIVAPreassolta));
					List<TitoliIVAPreassoltaAnnullati> titoliIVAPreassoltaAnnullati = ordinp.getTitoliIVAPreassoltaAnnullati();
					alimm.add( Utility.getTitoliIVAPreassoltaAnnullati(titoliIVAPreassoltaAnnullati));
					List<BigliettiAbbonamento> bigliettiAbbonamento = ordinp.getBigliettiAbbonamento();
					limm.add( Utility.getBigliettiAbbonamento(bigliettiAbbonamento));
					List<BigliettiAbbonamentoAnnullati> bigliettiAbbonamentoAnnullati = ordinp.getBigliettiAbbonamentoAnnullati();
					alimm.add(Utility.getBigliettiAbbonamentoAnnullati(bigliettiAbbonamentoAnnullati));
					List<AbbonamentiFissi> abbonamentiFissi = ordinp.getAbbonamentiFissi();
					limm.add(Utility.getAbbonamentiFissi(abbonamentiFissi));

				}
				ImmutableTriple<Integer, Integer, Integer> sum = Utility.sumImmutableTriple(limm);
				log.info("Vendite: [Quantità, LordoCorrispettivo, LordoPrevendita]  "+sum);
				rootv.add(sum);
				ImmutableTriple<Integer, Integer, Integer> asum = Utility.sumImmutableTriple(alimm);
				roota.add(asum);
				log.info("Annulli: [Quantità, LordoCorrispettivo, LordoPrevendita] "+asum);
			}

		}

		ImmutableTriple<Integer, Integer, Integer> rootsumv = Utility.sumImmutableTriple(rootv);
		ImmutableTriple<Integer, Integer, Integer> rootsuma = Utility.sumImmutableTriple(roota);
		LogRP.TitoliAccesso titoliAccesso = new LogRP.TitoliAccesso(rootsumv, rootsuma);

		ImmutableTriple<Integer, Integer, Integer> rootsumav = Utility.sumImmutableTriple(labb);
		ImmutableTriple<Integer, Integer, Integer> rootsumaa = Utility.sumImmutableTriple(alabb);
		LogRP.Abbonamenti abb = new LogRP.Abbonamenti(rootsumav, rootsumaa);

		LogRP l = new LogRP(titoliAccesso,abb);

		return l;

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiIVAPreassoltaAnnullati(
			List<AbbonamentiIVAPreassoltaAnnullati> abbonamentiIVAPreassoltaAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiIVAPreassoltaAnnullati titolo: abbonamentiIVAPreassoltaAnnullati) {
			corrispettivo = Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita = Integer.parseInt(titolo.getQuantita().trim());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiIVAPreassolta(List<AbbonamentiIVAPreassolta> abbonamentiIVAPreassolta) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiIVAPreassolta titolo: abbonamentiIVAPreassolta) {
			corrispettivo = Integer.parseInt(titolo.getImportoFiqurativo().trim());
			quantita = Integer.parseInt(titolo.getQuantita().trim());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);
	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiAnnullati(List<AbbonamentiAnnullati> abbonamentiAnnullati) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiAnnullati titolo: abbonamentiAnnullati) {
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}




	private static ImmutableTriple<Integer, Integer, Integer> getAbbonamentiEmessi(List<AbbonamentiEmessi> abbonamentiEmessi) {
		int corrispettivo = 0,quantita = 0,prevendita = 0;
		for(AbbonamentiEmessi titolo: abbonamentiEmessi) {
			corrispettivo += Integer.parseInt(titolo.getCorrispettivoLordo().trim());
			quantita += Integer.parseInt(titolo.getQuantita().trim());
			prevendita += Integer.parseInt(titolo.getPrevendita().trim());

		}
		return  ImmutableTriple.of(quantita, corrispettivo, prevendita);

	}

}
class XmlValidationEventHandler implements ValidationEventHandler {

	private  org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(XmlValidationEventHandler.class);
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
