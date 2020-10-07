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
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.Principal;
import java.security.PublicKey;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

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

import org.apache.commons.io.IOUtils;
import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.asn1.x500.style.BCStyle;
import org.bouncycastle.asn1.x500.style.IETFUtils;
import org.glassfish.grizzly.utils.Pair;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import cnr.isti.sse.big.data.transazioni.LogTransazione;



public class Utility {

	private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(Utility.class);




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

			Schema schema = schemaFactory.newSchema(new StreamSource(new StringReader(text), "xsdTop"));




			unmarshaller.setSchema(schema);
			unmarshaller.setEventHandler(new XmlValidationEventHandler());
		} catch (Exception e) {
			// TODO: handle exception
			log.error("XML non valido per xsd"+e.getMessage());
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
