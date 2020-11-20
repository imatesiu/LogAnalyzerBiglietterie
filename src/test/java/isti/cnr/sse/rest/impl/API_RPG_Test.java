package isti.cnr.sse.rest.impl;

import static org.junit.Assert.assertNotNull;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.Application;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import org.apache.commons.io.FileUtils;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;
import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.servlet.ServletContainer;
import org.glassfish.jersey.test.DeploymentContext;
import org.glassfish.jersey.test.JerseyTest;
import org.glassfish.jersey.test.ServletDeploymentContext;
import org.glassfish.jersey.test.TestProperties;
import org.glassfish.jersey.test.grizzly.GrizzlyWebTestContainerFactory;
import org.glassfish.jersey.test.spi.TestContainerFactory;
import org.junit.Test;


import cnr.isti.sse.big.rest.impl.ApiRestRPGBig;


public class API_RPG_Test extends JerseyTest {

	@Override
	protected TestContainerFactory getTestContainerFactory() {
		return new GrizzlyWebTestContainerFactory();
	}

	@Override
	protected DeploymentContext configureDeployment() {
		forceSet(TestProperties.CONTAINER_PORT, "0");
		return ServletDeploymentContext.forServlet(new ServletContainer(new ResourceConfig(MultiPartFeature.class).register(ApiRestRPGBig.class)))
				.build();

	}

	/*@Override
	protected Application configure() {
		return new ResourceConfig(ApiRestRPGBig.class).register(new MultiPartFeature());
	}*/

	@Override
	public void configureClient(ClientConfig config) {
		config.register(MultiPartFeature.class).register(ApiRestRPGBig.class);
	}

	@Test
	public void test() throws JAXBException, IOException, URISyntaxException, ClassNotFoundException {


		String Filexml = 	 "RPG_2020_11_06_001.xsi.p7m";

		//runTestRPM(Filexml);
		List<String> files = new ArrayList<String>();
		files.add(Filexml);
		files.add(Filexml);
		runTest3(files);

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




		File f = FileUtils.toFile( API_RPG_Test.class.getClassLoader().getResource(nameFilexml));
		//InputStream content = new FileInputStream(f);
		//final String read = ReaderWriter.readFromAsString(content, MediaType.APPLICATION_XML_TYPE);
		byte[] targetArray = fromFileToByteArray(f);

		final Entity<byte[]> rex = Entity.entity(targetArray, MediaType.MULTIPART_FORM_DATA);


		Response response = target("/biglietterie/RPG/").request(MediaType.APPLICATION_JSON).post(rex);



		/*String res2 = response.readEntity(new GenericType<String>() {
		});*/

		//System.out.print(res2);
		assertNotNull(response);
	}

	private void runTest3(List<String> files) throws IOException, ClassNotFoundException {
		MultiPart multipartEntity = new FormDataMultiPart();
		for(String nameFilexml: files) {
			File f = FileUtils.toFile( API_LTA_TEST.class.getClassLoader().getResource(nameFilexml));
			





			FileDataBodyPart filePart = new FileDataBodyPart("files", 
					f);

			filePart.setContentDisposition(
					FormDataContentDisposition.name("files")
					.fileName(f.getName()).build());
			
				multipartEntity.bodyPart(filePart);
			}
			Entity<MultiPart> entity = Entity.entity(multipartEntity, multipartEntity.getMediaType());
			//Entity<List<InputStream>> entity = Entity.entity(lbyte, MediaType.MULTIPART_FORM_DATA);
			Response response = target("/biglietterie/ListRiepilogoGiornaliero/").request(MediaType.APPLICATION_JSON).post(entity);



			String res2 = response.readEntity(new GenericType<String>() {
			});

			System.out.print(res2);
			assertNotNull(response);
		
	}




}
