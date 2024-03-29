package isti.cnr.sse.rest.impl;

import static org.junit.Assert.assertNotNull;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringReader;
import java.net.URISyntaxException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.security.Principal;
import java.security.PublicKey;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import javax.xml.crypto.dsig.Reference;
import javax.xml.crypto.dsig.XMLSignature;
import javax.xml.crypto.dsig.XMLSignatureFactory;
import javax.xml.crypto.dsig.dom.DOMValidateContext;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMResult;
import javax.xml.transform.stream.StreamSource;

import org.apache.commons.io.FileUtils;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;
import org.glassfish.jersey.message.internal.ReaderWriter;
import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.servlet.ServletContainer;
import org.glassfish.jersey.test.DeploymentContext;
import org.glassfish.jersey.test.JerseyTest;
import org.glassfish.jersey.test.ServletDeploymentContext;
import org.glassfish.jersey.test.TestProperties;
import org.glassfish.jersey.test.grizzly.GrizzlyWebTestContainerFactory;
import org.glassfish.jersey.test.spi.TestContainerFactory;
import org.junit.Test;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.rest.impl.ApiRestEsameComplessivo;


public class API_EsameComplessivo_TEST extends JerseyTest {

	@Override
	protected TestContainerFactory getTestContainerFactory() {
		return new GrizzlyWebTestContainerFactory();
	}

	@Override
	protected DeploymentContext configureDeployment() {
		forceSet(TestProperties.CONTAINER_PORT, "0");
		//register(MultiPartFeature.class);
		return ServletDeploymentContext.forServlet(new ServletContainer(new ResourceConfig(MultiPartFeature.class).register(ApiRestEsameComplessivo.class)))
				.build();

	}
	


	/*@Override
	protected Application configure() {
		return new ResourceConfig(ApiRestLogAccessi.class);//.register(new MultiPartFeature());
	}*/
	
	@Override
    public void configureClient(ClientConfig config) {
        config.register(MultiPartFeature.class).register(ApiRestEsameComplessivo.class);
    }


	@Test
	public void test() throws ClassNotFoundException, IOException  {
		
		
		
		//String nameFilexml = "log.xml";//

		List<String> files = new ArrayList<String>();
	//runTest(nameFilexml);
	
		//String Filexml = "es1/RPM_2020_10_00_001.xsi.p7m";
		//files.add(Filexml);
		/*String Filexml = "es1/RPG_2020_10_17_001.xsi.p7m";
		files.add(Filexml);
		 Filexml = "es1/LOG_2020_10_17_001.xsi.p7m";
		files.add(Filexml);*/
		
		// Filexml = "es1/LOG_2020_10_16_001.xsi.p7m";
		//files.add(Filexml);
		
	/*String Filexml = "es2/LOG_2020_11_05_001.xsi.p7m";
	//runTest2(Filexml);*/
		String Filexml = "es3/RPM_2020_11_00_001.xsi.p7m";
	
	files.add(Filexml);
	 Filexml = "es2/LOG_2020_11_05_001.xsi.p7m";
	//files.add(Filexml);
	/*Filexml = "es2/LTA_2020_11_05_001.xsi.p7m";
	files.add(Filexml);
	Filexml = "es2/LTA_2020_11_06_001.xsi.p7m";
	files.add(Filexml);
	Filexml = "es2/RPM_2020_11_00_002.xsi.p7m";
	files.add(Filexml);*/
	
	runTest3(files);
	/*File f = FileUtils.toFile( APIProveHWImplTest.class.getClassLoader().getResource(Filexml));
	//InputStream content = new FileInputStream(f);
	//final String read = ReaderWriter.readFromAsString(content, MediaType.APPLICATION_XML_TYPE);
	
	
	
	byte[] targetArray = fromFileToByteArray(f);
	
	byte[] t = 	Utility.getData(targetArray);
	String string = new String(t);
    //System.out.println(string);
	Store<X509CertificateHolder> cert = Utility.getCert(targetArray);
	
	try {
	 boolean	result = Utility.verifyPKCS7(targetArray,t);
	 System.out.println(result);
	} catch (CertificateException | StoreException | OperatorCreationException | NoSuchAlgorithmException
			| NoSuchProviderException | InvalidNameException | CMSException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	
	System.out.println("");*/
	}

	
	
	private void runTest3(List<String> files) throws IOException, ClassNotFoundException {
		MultiPart multipartEntity = new FormDataMultiPart();
		for(String nameFilexml: files) {
			File f = FileUtils.toFile( API_EsameComplessivo_TEST.class.getClassLoader().getResource(nameFilexml));
			

			assertNotNull(f);



			FileDataBodyPart filePart = new FileDataBodyPart("files", 
					f);

			filePart.setContentDisposition(
					FormDataContentDisposition.name("files")
					.fileName(f.getName()).build());
			
				multipartEntity.bodyPart(filePart);
			}
			Entity<MultiPart> entity = Entity.entity(multipartEntity, multipartEntity.getMediaType());
			//Entity<List<InputStream>> entity = Entity.entity(lbyte, MediaType.MULTIPART_FORM_DATA);
			Response response = target("/biglietterie/EsameComplessivo/").request(MediaType.APPLICATION_JSON).post(entity);



			String res2 = response.readEntity(new GenericType<String>() {
			});


			assertNotNull(response);
		
	}

	private byte[] fromFileToByteArray(File file) {
	    try {
	        return FileUtils.readFileToByteArray(file);
	    } catch (IOException e) {
	    	System.err.println("Error while reading .p7m file!" + e);
	    }
	    return new byte[0];
	}

	
	
	
	private void runTest2(String nameFilexml) throws JAXBException, IOException, URISyntaxException {
		
		


		File f = FileUtils.toFile( API_EsameComplessivo_TEST.class.getClassLoader().getResource(nameFilexml));
		InputStream content = new FileInputStream(f);
		//final String read = ReaderWriter.readFromAsString(content, MediaType.APPLICATION_XML_TYPE);
		byte[] targetArray = fromFileToByteArray(f);
		
		final Entity<byte[]> rex = Entity.entity(targetArray, MediaType.MULTIPART_FORM_DATA);


		Response response = target("/biglietterie/LogTransazione/").request(MediaType.MULTIPART_FORM_DATA).post(rex);



		String res2 = response.readEntity(new GenericType<String>() {
		});
		

		assertNotNull(response);
	}
	
	
	private void runTest(String nameFilexml) throws JAXBException, IOException, URISyntaxException {
		
		
		
		InputStream is = API_EsameComplessivo_TEST.class.getClassLoader().getResourceAsStream(nameFilexml);
		assertNotNull(is);
		JAXBContext jaxbContexti = JAXBContext.newInstance(LogTransazione.class);

		Unmarshaller jaxbUnmarshaller1 = jaxbContexti.createUnmarshaller();
		LogTransazione collaborativeContentInput = (LogTransazione) jaxbUnmarshaller1.unmarshal(is);
		//getMatricola(collaborativeContentInput);
		Entity<LogTransazione> entity = Entity.entity(collaborativeContentInput, MediaType.APPLICATION_XML);


		File f = FileUtils.toFile( API_EsameComplessivo_TEST.class.getClassLoader().getResource(nameFilexml));
		InputStream content = new FileInputStream(f);
		final String read = ReaderWriter.readFromAsString(content, MediaType.APPLICATION_XML_TYPE);

		final Entity<String> rex = Entity.entity(read, MediaType.APPLICATION_XML_TYPE);


		Response response = target("/biglietterie/LogTransazione/").request(MediaType.APPLICATION_XML).post(rex);



		String res2 = response.readEntity(new GenericType<String>() {
		});
		

		assertNotNull(response);
	}

	
	private String stringtoStreaming(InputStream inputStream){

		StringBuilder textBuilder = new StringBuilder();
		try{ 
			try (Reader reader = new BufferedReader(new InputStreamReader
					(inputStream, Charset.forName(StandardCharsets.UTF_8.name())))) {
				int c = 0;
				while ((c = reader.read()) != -1) {
					textBuilder.append((char) c);
				}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		return textBuilder.toString();
	}


	private boolean statusCertificateAndSignature(byte[] certificate, String Document) {

		//byte[] certificate = d.getSignature().getKeyInfo().getX509Data().getX509Certificate();
		CertificateFactory fact = null;
		try {
			fact = CertificateFactory.getInstance("X.509");

			X509Certificate cert = (X509Certificate) fact
					.generateCertificate(new ByteArrayInputStream(certificate));

			PublicKey publicKey = cert.getPublicKey();

			Document doc = convertStringToDocument(Document);// marshallToDocument(d,DatiCorrispettiviType.class);

			NodeList nl = doc.getElementsByTagNameNS(XMLSignature.XMLNS, "Signature");

			if (nl.getLength() == 0) {
				throw new Exception("Cannot find Signature element");
			}

			DOMValidateContext valContext = new DOMValidateContext(publicKey, nl.item(0));

			XMLSignatureFactory fac = XMLSignatureFactory.getInstance("DOM");

			XMLSignature signature = fac.unmarshalXMLSignature(valContext);

			boolean validFlag = signature.validate(valContext);

			// Check core validation status.
			if (validFlag == false) {
				
				System.err.println("Signature failed core validation");
				boolean sv = signature.getSignatureValue().validate(valContext);
				System.out.println("signature validation status: " + sv);
				if (sv == false) {
					// Check the validation status of each Reference.
					Iterator i = signature.getSignedInfo().getReferences().iterator();
					for (int j = 0; i.hasNext(); j++) {
						boolean refValid = ((Reference) i.next()).validate(valContext);
						System.out.println("ref[" + j + "] validity status: " + refValid);
					}
				}
			} else {
				System.out.println("Signature passed core validation");
			}

			Principal principal = cert.getSubjectDN();
			String name = principal.getName();
			return validFlag;

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return false;

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

}
