package isti.cnr.sse.rest.impl;

import static org.junit.Assert.assertNotNull;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
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
		return ServletDeploymentContext.forServlet(new ServletContainer(new ResourceConfig(ApiRestRPGBig.class).register(MultiPartFeature.class)))
				.build();

	}

	@Override
	protected Application configure() {
		return new ResourceConfig(ApiRestRPGBig.class).register(new MultiPartFeature());
	}

	@Override
	public void configureClient(ClientConfig config) {
		config.register(MultiPartFeature.class);
	}

	@Test
	public void test() throws JAXBException, IOException, URISyntaxException {


		String Filexml = "RPG_2020_10_13_001.xsi.p7m";
		runTestRPM(Filexml);

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


		Response response = target("/biglietterie/RPG/").request(MediaType.MULTIPART_FORM_DATA).post(rex);



		String res2 = response.readEntity(new GenericType<String>() {
		});


		assertNotNull(response);
	}

	private void runTestRPM(List<String> files) throws JAXBException, IOException, URISyntaxException {

		MultiPart multipartEntity = new FormDataMultiPart();
		for(String nameFilexml: files) {


			File f = FileUtils.toFile( API_RPG_Test.class.getClassLoader().getResource(nameFilexml));

			FileDataBodyPart filePart = new FileDataBodyPart("files", 
					f);

			filePart.setContentDisposition(
					FormDataContentDisposition.name("files")
					.fileName(f.getName()).build());
			
				multipartEntity.bodyPart(filePart);
			}
			

		Entity<MultiPart> entity = Entity.entity(multipartEntity, multipartEntity.getMediaType());

		Response response = target("/biglietterie/RPG/").request(MediaType.MULTIPART_FORM_DATA).post(entity);



		String res2 = response.readEntity(new GenericType<String>() {
		});


		assertNotNull(response);
	}




}
