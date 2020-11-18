package isti.cnr.sse.rest.impl;

import static org.junit.Assert.*;

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
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.Principal;
import java.security.PublicKey;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Collection;
import java.util.Iterator;

import javax.naming.InvalidNameException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.Application;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
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
import org.apache.commons.io.IOUtils;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cms.CMSException;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.util.Store;
import org.bouncycastle.util.StoreException;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
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
import cnr.isti.sse.big.rest.impl.ApiRestLogBig;
import cnr.isti.sse.big.rest.impl.ApiRestRPMBig;
import cnr.isti.sse.big.util.Utility;


public class API_RPM_Test extends JerseyTest {

	@Override
	protected TestContainerFactory getTestContainerFactory() {
		return new GrizzlyWebTestContainerFactory();
	}

	@Override
	protected DeploymentContext configureDeployment() {
		forceSet(TestProperties.CONTAINER_PORT, "0");
		return ServletDeploymentContext.forServlet(new ServletContainer(new ResourceConfig(ApiRestRPMBig.class).register(new MultiPartFeature())))
				.build();

	}

	@Override
	protected Application configure() {
		return new ResourceConfig(ApiRestLogBig.class).register(new MultiPartFeature());
	}
	
	@Override
    public void configureClient(ClientConfig config) {
        config.register(MultiPartFeature.class);
    }

	@Test
	public void test() throws JAXBException, IOException, URISyntaxException {
		
		
		
		//String nameFilexml = "log.xml";//

		
	//runTest(nameFilexml);
	

	
	String Filexml = "RPM_2020_10_00_001.xsi.p7m";
	runTestRPM(Filexml);
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

	private byte[] fromFileToByteArray(File file) {
	    try {
	        return FileUtils.readFileToByteArray(file);
	    } catch (IOException e) {
	    	System.err.println("Error while reading .p7m file!" + e);
	    }
	    return new byte[0];
	}

	private void runTestRPM(String nameFilexml) throws JAXBException, IOException, URISyntaxException {
		
		


		File f = FileUtils.toFile( API_RPM_Test.class.getClassLoader().getResource(nameFilexml));
		//InputStream content = new FileInputStream(f);
		//final String read = ReaderWriter.readFromAsString(content, MediaType.APPLICATION_XML_TYPE);
		byte[] targetArray = fromFileToByteArray(f);
		
		final Entity<byte[]> rex = Entity.entity(targetArray, MediaType.MULTIPART_FORM_DATA);


		Response response = target("/biglietterie/RPM/").request(MediaType.MULTIPART_FORM_DATA).post(rex);



		String res2 = response.readEntity(new GenericType<String>() {
		});
		

		assertNotNull(response);
	}
	
	


}
